import os
from pathlib import Path
import sys
import json
from time import sleep
from PySide2.QtCore import QObject, Slot, Signal
from src.dataManager import DataManager
from src.apiManager import ApiManager
from src.stateManager import StateManager
from src.modbusManager import ModbusManager
from threading import Thread
import datetime

class BackendManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.dbManager = DataManager()
        self.apiManager = ApiManager()
        self.stateManager = StateManager()
        self.modbusManager = ModbusManager(self)
        self.apiManager.listen()
        self.cardKey = ''
        self.cardThreadAlive = False
        self.cardKeyThread = None
        self.cardKeyLastRead = datetime.datetime.now()

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


    # MODBUS HANDLERS
    def onServiceFlagActivated(self):
        self.serviceScreenRequested.emit()


    # SLOTS
    @Slot()
    def appIsClosing(self):
        self.__stopApiManager()
        self.__stopModbusManager()


    @Slot()
    def checkMachineConfig(self):
        self.checkConfigResult.emit(self.dbManager.checkMachineConfig())

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
            loginResult = self.stateManager.loginByCard(self.cardKey)
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
        data = self.dbManager.getItemCategories()
        if data:
            for d in data:
                creditInfo = self.dbManager.getCreditInfo(self.stateManager.userData['id'], int(d['Id']))
                if creditInfo:
                    d['ActiveCredit'] = creditInfo['ActiveCredit']
                else:
                    d['ActiveCredit'] = 0

            self.getItemCategories.emit(json.dumps(data))


    @Slot(int)
    def storeSelectedItemCategory(self, categoryId):
        self.stateManager.selectedCategoryId = categoryId


    @Slot()
    def requestItemGroups(self):
        if self.stateManager.selectedCategoryId:
            groupsData = self.dbManager.getItemGroups(self.stateManager.selectedCategoryId)
            if groupsData:
                categoryObj = self.dbManager.getItemCategory(self.stateManager.selectedCategoryId)
                self.getItemGroups.emit(json.dumps({ 'categoryName': categoryObj['ItemCategoryName'], 'groups': groupsData }))


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


    @Slot(int)
    def storeSelectedItem(self, itemId):
        self.stateManager.selectedItemId = itemId


    @Slot()
    def requestProperSpirals(self):
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

        if self.stateManager.selectedItemId:
            itemData = self.dbManager.getItem(self.stateManager.selectedItemId)
            if itemData:
                spiralDesign['ItemName'] = itemData['ItemName']

            spiralData = self.dbManager.getProperSpirals(self.stateManager.selectedItemId)
            if spiralData and len(spiralData) > 0:
                spiralDesign["RelatedSpirals"] = spiralData

            allSpirals = self.dbManager.getAllSpirals()
            if allSpirals:
                spiralDesign['AllSpirals'] = allSpirals

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
            spiralInfo = self.dbManager.getSpiralInfo(spiralNo)
            if spiralInfo is None:
                raise Exception("Spiral bilgisi bulunamadı.")

            hasRights = self.dbManager.checkEmployeeHasCredit(int(self.stateManager.userData['id']), 
                int(spiralInfo['ItemCategoryId']) if spiralInfo['ItemCategoryId'] else 0,
                int(spiralInfo['ItemGroupId']) if spiralInfo['ItemGroupId'] else None)
            if not hasRights:
                raise Exception("Bu ürün için yeterli krediniz bulunmamaktadır.")
            else:
                tryCount = 0
                pushResult = self.modbusManager.pushItem(spiralNo)
                while pushResult == False and tryCount < 3:
                    sleep(1)
                    pushResult = self.modbusManager.pushItem(spiralNo)
                    tryCount = tryCount + 1

                if pushResult == False:
                    raise Exception("Cihaz iletişiminde bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.")
                else:
                    postResult = self.apiManager.sendSpiralConsuming({
                        'employeeId': self.stateManager.userData['id'],
                        'itemId': spiralInfo['ItemId'],
                        'spiralNo': int(spiralNo)
                    })
                    self.dbManager.consumeCredit(int(self.stateManager.userData['id']), 
                        int(spiralInfo['ItemCategoryId']), 1 if postResult else 0)
                    self.getPushSpiralResult.emit(json.dumps({ "Result": True }))
        except Exception as e:
            self.getPushSpiralResult.emit(json.dumps({ "Result": False, "ErrorMessage": str(e) }))
            
        self.stateManager.pushProcessFinished = True
        
    
    @Slot()
    def requestActiveCredit(self):
        if self.stateManager.selectedCategoryId > 0:
            creditInfo = self.dbManager.getCreditInfo(self.stateManager.userData['id'], 
                self.stateManager.selectedCategoryId, self.stateManager.selectedGroupId)
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
            creditInfo = self.dbManager.getCreditInfo(self.stateManager.userData['id'],
                itemCategoryId)
            if creditInfo:
                self.getCredit.emit(json.dumps(creditInfo))