import os
from pathlib import Path
import sys
import json
from time import sleep
from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine
from src.hkThread import HekaThread
from src.dataManager import DataManager
from src.apiManager import ApiManager
from src.stateManager import StateManager
from src.modbusManager import ModbusManager
from threading import Thread
import datetime


class BackendManager(QObject):
    def __init__(self, appObject):
        QObject.__init__(self)
        self.__app = appObject
        self.dbManager = DataManager()
        self.apiManager = ApiManager(self)
        self.stateManager = StateManager()
        self.modbusManager = ModbusManager(self)
        self.apiManager.listen()
        self.cardKey = ''
        self.cardThreadAlive = False
        self.cardKeyThread = None
        self.cardKeyLastRead = datetime.datetime.now()
        self.lastLiveTime = datetime.datetime.now()
        self.currentSpirals = []
        self.runLiveListener = True
        self.liveListenerThread = HekaThread(target=self.__loopLiveListener)
        self.liveListenerThread.start()

    def __stopApiManager(self):
        if self.apiManager:
            try:
                self.apiManager.stop()
            except:
                pass

    
    def __stopModbusManager(self):
        if self.modbusManager:
            try:
                self.modbusManager.stop()
            except:
                pass


    # SIGNALS
    configSaved = Signal(bool)
    checkConfigResult = Signal(bool)
    cardLoggedIn = Signal(bool)
    userLoggedOut = Signal()
    getUserData = Signal(str)
    getMachineConfig = Signal(str)
    serviceScreenRequested = Signal()
    getItemCategories = Signal(str)
    getItemGroups = Signal(str)
    getItems = Signal(str)
    getProperSpirals = Signal(str)
    getAllSpirals = Signal(str)
    getPushSpiralResult = Signal(str)
    getActiveCredit = Signal(str)
    getCredit = Signal(str)
    getNewVideo = Signal()
    startNewVideo = Signal()
    clientTimedOut = Signal()
    appCloseRequested = Signal()
    oskRequested = Signal()
    oskClosed = Signal()
    backendProcStarted = Signal()
    backendProcFinished = Signal()


    # MODBUS HANDLERS
    def onServiceFlagActivated(self):
        self.serviceScreenRequested.emit()

    def __loopLiveListener(self):
        while self.runLiveListener == True:
            dtNow = datetime.datetime.now()
            totalDiffSec = (dtNow - self.lastLiveTime).total_seconds()
            
            if totalDiffSec >= 15:
                self.clientTimedOut.emit()
                self.lastLiveTime = datetime.datetime.now()
            
            sleep(1)

    # PUBLIC METHODS
    def raiseNewVideoArrived(self):
        self.getNewVideo.emit()


    def raiseStartNewVideo(self):
        self.startNewVideo.emit()
        

    # SLOTS
    @Slot()
    def appIsClosing(self):
        self.cardThreadAlive = False
        self.__stopApiManager()
        self.__stopModbusManager()
        self.runLiveListener = False
        try:
            if self.liveListenerThread:
                self.liveListenerThread.stop()
            sys.exit()
        except:
            pass


    @Slot(bool)
    def requestOsk(self, oskStatus):
        if oskStatus == True:
            tmpThr = HekaThread(target=self.__runEnableOsk)
            tmpThr.start()
        else:
            self.oskClosed.emit()

    
    def __runEnableOsk(self):
        sleep(0.2)
        self.oskRequested.emit()


    @Slot()
    def restartApp(self):
        pass


    @Slot()
    def closeApp(self):
        self.appCloseRequested.emit()


    @Slot()
    def updateLiveSignal(self):
        self.lastLiveTime = datetime.datetime.now()


    @Slot()
    def checkMachineConfig(self):
        res = self.dbManager.checkMachineConfig()
        # self.apiManager.updateVideo()
        self.checkConfigResult.emit(res)


    # BEGIN -- CARD READING AND STATE MANAGEMENT SLOTS
    @Slot(str)
    def cardReading(self, readText):
        self.cardKey += readText
        self.cardKeyLastRead = datetime.datetime.now()
        if not self.cardThreadAlive:
            self.cardKey = readText
            self.cardKeyThread = Thread(target=self.__cardReadLoop)
            self.cardKeyThread.start()

    def __cardReadLoop(self):
        self.cardThreadAlive = True
        while (datetime.datetime.now() - self.cardKeyLastRead).total_seconds() * 1000 <= 750:
            pass
        if len(self.cardKey) > 0:
            self.backendProcStarted.emit()
            loginResult = self.stateManager.loginByCard(self.cardKey)
            self.backendProcFinished.emit()
            self.cardLoggedIn.emit(loginResult)
            self.cardKey = ''
        self.cardThreadAlive = False
        self.cardKey = ''

    @Slot()
    def requestUserData(self):
        userObj = self.stateManager.getUserData()
        self.getUserData.emit(json.dumps(userObj))
    

    @Slot()
    def requestLogout(self):
        self.stateManager.logout()
        self.userLoggedOut.emit()
    # END -- CARD READING AND STATE MANAGEMENT SLOTS

    @Slot()
    def requestMachineConfig(self):
        confObj = self.dbManager.getMachineConfig()
        self.getMachineConfig.emit(json.dumps(confObj))


    @Slot(str)
    def saveMachineConfig(self, config):
        confObj = json.loads(config)
        saveResult = self.dbManager.saveMachineConfig(confObj)
        self.configSaved.emit(saveResult)

    # ITEM CATEGORY & GROUP REQUESTS
    @Slot()
    def requestItemCategories(self):
        # self.backendProcStarted.emit()
        userData = self.stateManager.getUserData()
        self.apiManager.fetchCredits(userData['id'])

        data = self.apiManager.getItemCategories()
        # self.backendProcFinished.emit()
        self.getItemCategories.emit(json.dumps(data))

        # data = self.dbManager.getProperItemCategories(self.stateManager.userData['id'])
        # if data:
        #     for d in data:
        #         creditInfo = self.dbManager.getCreditInfo(self.stateManager.userData['id'], int(d['Id']))
        #         if creditInfo:
        #             d['ActiveCredit'] = creditInfo['ActiveCredit']
        #         else:
        #             d['ActiveCredit'] = 0

        #     self.getItemCategories.emit(json.dumps(data))


    @Slot(int)
    def storeSelectedItemCategory(self, categoryId):
        self.stateManager.selectedCategoryId = categoryId


    @Slot()
    def requestItemGroups(self):
        if self.stateManager.selectedCategoryId:
            data = self.apiManager.getItemGroups(self.stateManager.selectedCategoryId)
            self.getItemGroups.emit(json.dumps({ 'categoryName': '', 'groups': data }))
        # if self.stateManager.selectedCategoryId:
        #     groupsData = self.dbManager.getItemGroups(self.stateManager.selectedCategoryId)
        #     if groupsData:
        #         categoryObj = self.dbManager.getItemCategory(self.stateManager.selectedCategoryId)
        #         self.getItemGroups.emit(json.dumps({ 'categoryName': categoryObj['ItemCategoryName'], 'groups': groupsData }))


    @Slot()
    def requestProperItemGroups(self):
        # self.backendProcStarted.emit()
        if self.stateManager.selectedCategoryId:
            data = self.apiManager.getItemGroups(self.stateManager.selectedCategoryId)
            self.getItemGroups.emit(json.dumps({ 'categoryName': data['categoryName'], 'groups': data['groups'] }))

        # self.backendProcFinished.emit()
        # if self.stateManager.selectedCategoryId:
        #     groupsData = self.dbManager.getProperItemGroups(self.stateManager.selectedCategoryId, self.stateManager.userData['id'])
        #     if groupsData:
        #         categoryObj = self.dbManager.getItemCategory(self.stateManager.selectedCategoryId)
        #         self.getItemGroups.emit(json.dumps({ 'categoryName': categoryObj['ItemCategoryName'], 'groups': groupsData }))


    @Slot(int)
    def storeSelectedItemGroup(self, groupId):
        self.stateManager.selectedGroupId = groupId


    @Slot()
    def requestItems(self):
        if self.stateManager.selectedGroupId:
            itemsData = self.dbManager.getItems(self.stateManager.selectedGroupId)
            if itemsData:
                groupObj = self.dbManager.getItemGroup(self.stateManager.selectedGroupId)
                self.getItems.emit(json.dumps({ 
                    'groupName': groupObj['ItemGroupName'],
                    'groupImage': groupObj['GroupImage'],
                    'items': itemsData }))


    @Slot()
    def requestProperItems(self):
        # self.backendProcStarted.emit()
        if self.stateManager.selectedGroupId:
            data = self.apiManager.getItems(self.stateManager.selectedCategoryId, self.stateManager.selectedGroupId)
            self.getItems.emit(json.dumps({ 
            'groupName': data['groupName'], 
            'groupImage': '',
            'items': data['items'] }))

        # self.backendProcFinished.emit()

        # if self.stateManager.selectedGroupId:
        #     itemsData = self.dbManager.getProperItems(self.stateManager.selectedGroupId, self.stateManager.selectedCategoryId, self.stateManager.userData['id'])
        #     if itemsData:
        #         groupObj = self.dbManager.getItemGroup(self.stateManager.selectedGroupId)
        #         self.getItems.emit(json.dumps({ 
        #             'groupName': groupObj['ItemGroupName'], 
        #             'groupImage': groupObj['GroupImage'],
        #             'items': itemsData }))




    @Slot(int)
    def storeSelectedItem(self, itemId):
        self.stateManager.selectedItemId = itemId


    @Slot()
    def requestProperSpirals(self):
        # self.backendProcStarted.emit()

        spiralDesign = {
            "Rows": 0,
            "Cols": 0,
            "RelatedSpirals": [],
            "ItemName": "",
            "AllSpirals": [],
        }

        machineContent = self.apiManager.getMachineInfo() # self.dbManager.getMachineConfig()
        if machineContent:
            spiralDesign["Rows"] = int(machineContent['Rows'])
            spiralDesign["Cols"] = int(machineContent['Cols'])

        if self.stateManager.selectedItemId:
            data = self.apiManager.getSpirals(self.stateManager.selectedItemId)
            spiralDesign['RelatedSpirals'] = list(filter(lambda d: d['itemId'] == self.stateManager.selectedItemId, data['spirals']))
            spiralDesign['AllSpirals'] = data['spirals']
            spiralDesign['ItemName'] = data['itemName']
            self.currentSpirals = data['spirals']

        # if self.stateManager.selectedItemId:
        #     itemData = self.dbManager.getItem(self.stateManager.selectedItemId)
        #     if itemData:
        #         spiralDesign['ItemName'] = itemData['ItemName']

        #     spiralData = self.dbManager.getProperSpirals(self.stateManager.selectedItemId)
        #     if spiralData and len(spiralData) > 0:
        #         spiralDesign["RelatedSpirals"] = spiralData

        #     allSpirals = self.dbManager.getAllSpirals()
        #     if allSpirals:
        #         spiralDesign['AllSpirals'] = allSpirals

        # self.backendProcFinished.emit()

        self.getProperSpirals.emit(json.dumps(spiralDesign))


    @Slot()
    def requestAllSpirals(self):
        spiralDesign = {
            "Rows": 0,
            "Cols": 0,
            "RelatedSpirals": [],
            "ItemName": "",
            "AllSpirals": [],
        }

        machineContent = self.dbManager.getMachineConfig()
        if machineContent:
            spiralDesign["Rows"] = int(machineContent['Rows'])
            spiralDesign["Cols"] = int(machineContent['Cols'])

        allSpirals = self.dbManager.getAllSpirals()
        if allSpirals:
            spiralDesign['AllSpirals'] = allSpirals

        self.getAllSpirals.emit(json.dumps(spiralDesign))


    @Slot(int)
    def requestPushSpiral(self, spiralNo):
        if not self.stateManager.pushProcessFinished:
            return
        
        self.stateManager.pushProcessFinished = False

        try:
            spiralInfo = list(filter(lambda d: int(d['posOrders']) == int(spiralNo), self.currentSpirals))[0] # self.dbManager.getSpiralInfo(spiralNo)
            if spiralInfo is None:
                raise Exception("Spiral bilgisi bulunamadı.")

            # hasRights = False
            # self.dbManager.checkEmployeeHasCredit(int(self.stateManager.userData['id']), 
            #     int(spiralInfo['ItemCategoryId']) if spiralInfo['ItemCategoryId'] else 0,
            #     int(spiralInfo['ItemGroupId']) if spiralInfo['ItemGroupId'] else None)

            hasRights = self.apiManager.checkCredits({
                        'employeeId': self.stateManager.userData['id'],
                        'itemId': spiralInfo['itemId'],
                        'spiralNo': int(spiralNo)
                    })

            if not hasRights[0]:
                raise Exception(hasRights[1])
            else:
                # tryCount = 0
                pushResult = self.modbusManager.pushItem(spiralNo)
                # while pushResult == False and tryCount < 1:
                #     sleep(1)
                #     pushResult = self.modbusManager.pushItem(spiralNo)
                #     tryCount = tryCount + 1
                if pushResult['Result'] == False:
                    raise Exception(pushResult['ErrorMessage'])
                else:
                    postResult = self.apiManager.sendSpiralConsuming({
                        'employeeId': self.stateManager.userData['id'],
                        'itemId': spiralInfo['itemId'],
                        'spiralNo': int(spiralNo)
                    })
                    # self.dbManager.consumeCredit(int(self.stateManager.userData['id']), 
                    #     int(spiralInfo['itemCategoryId']), 1 if postResult else 0)
                    self.getPushSpiralResult.emit(json.dumps({ "Result": True }))
        except Exception as e:
            self.getPushSpiralResult.emit(json.dumps({ "Result": False, "ErrorMessage": str(e) }))
            
        self.stateManager.pushProcessFinished = True
        
    
    @Slot()
    def requestActiveCredit(self):
        if self.stateManager.selectedCategoryId > 0:
            creditInfo = self.apiManager.getCreditInfo(self.stateManager.userData['id'], 
                 self.stateManager.selectedCategoryId, self.stateManager.selectedGroupId, self.stateManager.selectedItemId)
            # self.dbManager.getCreditInfo(self.stateManager.userData['id'], 
            #     self.stateManager.selectedCategoryId, self.stateManager.selectedGroupId, self.stateManager.selectedItemId)
            if creditInfo:
                rangeDesc = ''
                rangeCredit = 0

                if creditInfo['RangeType'] == 1:
                    rangeDesc = 'Günlük'
                elif creditInfo['RangeType'] == 2:
                    rangeDesc = 'Haftalık'
                elif creditInfo['RangeType'] == 3:
                    rangeDesc = 'Aylık'

                if creditInfo['RangeLength'] and int(creditInfo['RangeLength']) > 1:
                    rangeDesc = str(creditInfo['RangeLength']) + ' ' + rangeDesc

                rangeCredit = int(creditInfo['CreditByRange']) if creditInfo['CreditByRange'] else 0
                creditInfo['CreditRange'] = {
                    'RangeType': rangeDesc,
                    'RangeCredit': rangeCredit,
                }

                self.getActiveCredit.emit(json.dumps(creditInfo))


    @Slot(int)
    def requestCredit(self, itemCategoryId):
        if itemCategoryId > 0:
            creditInfo = self.apiManager.getCreditInfo(self.stateManager.userData['id'],
                itemCategoryId)
            # creditInfo = self.dbManager.getCreditInfo(self.stateManager.userData['id'],
            #     itemCategoryId)
            if creditInfo:
                self.getCredit.emit(json.dumps(creditInfo))