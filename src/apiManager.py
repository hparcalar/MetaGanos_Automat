from src.dataManager import DataManager
from threading import Thread
from src.hkThread import HekaThread
from time import sleep
from datetime import datetime
from os.path import isfile, getmtime
import os
import json
import requests

class ApiManager():
    def __init__(self, backend):
        self._backend = backend
        self.dbManager = DataManager()
        self.mustRun = False
        self.apiUri = ''
        self.token = ''
        self.dealerCode = ''
        self.plantCode = ''
        self.machineId = 0
        self.configData = {}
        self.runner = HekaThread(target=self.__runnerLoop)


    def listen(self):
        self.mustRun = True
        self.runner.start()


    def __obtainToken(self):
        try:
            self.dealerCode = self.configData['DealerCode']
            self.plantCode = self.configData['PlantCode']

            resp = requests.post(self.apiUri + 'User/LoginMachine', json={
                'login': self.configData['Code'],
                'password': '',
                'dealerCode': self.dealerCode,
                'plantCode': self.plantCode,
            })

            if resp.status_code == 200:
                self.token = resp.text
                
                respId = requests.post(self.apiUri + 'User/MachineId', json={
                    'login': self.configData['Code'],
                    'password': '',
                    'dealerCode': self.dealerCode,
                    'plantCode': self.plantCode,
                })
                if respId.status_code == 200:
                    self.machineId = int(respId.text)
        except:
            pass


    def __updateEmployees(self): 
        try:
            resp = requests.get(self.apiUri + 'Employee', 
                headers={ "Authorization": "Bearer " + self.token })

            if resp.status_code == 200:
                data = resp.json()
                for d in data:
                    saveResult = self.dbManager.saveEmployee(d)
                    if saveResult:
                        respDetail = requests.get(self.apiUri + 'Employee/' + str(d['id']),
                            headers={ "Authorization": "Bearer " + self.token })
                        if respDetail.status_code == 200:
                            detailData = respDetail.json()
                            self.dbManager.saveCredits(int(d['id']), detailData['credits'])

        except Exception as e:
            pass


    def __updateItemCategories(self):
        try:
            plantId = None
            respFindPlant = requests.get(self.apiUri + 'Plant/Find/' + self.dealerCode + '/' + self.plantCode,
                headers={ "Authorization": "Bearer " + self.token })
            if respFindPlant.status_code == 200:
                data = respFindPlant.json()
                plantId = data['id']

            if plantId:
                resp = requests.get(self.apiUri + 'Plant/' + str(plantId) + '/ItemCategories', 
                    headers={ "Authorization": "Bearer " + self.token })

                if resp.status_code == 200:
                    data = resp.json()

                    existingData = self.dbManager.getItemCategories()
                    deletedData = list(filter(lambda d: len(list(filter(lambda c: c['id'] == d['Id'], data))) == 0 ,existingData))
                    if deletedData and len(deletedData) > 0:
                        for dl in deletedData:
                            self.dbManager.deleteItemCategory(dl['Id'])

                    for d in data:
                        try:
                            respDetail = requests.get(self.apiUri + 'ItemCategory/' + str(d['id']), 
                                headers={ "Authorization": "Bearer " + self.token })
                            if respDetail.status_code == 200:
                                detailObj = respDetail.json()
                                self.dbManager.saveItemCategory(detailObj)
                        except:
                            pass

        except Exception as e:
            print(e)
            pass

    
    def __updateItemGroups(self):
        try:
            categoryList = self.dbManager.getItemCategories()

            for cat in categoryList:
                resp = requests.get(self.apiUri + 'ItemCategory/' + str(cat['Id']) + '/Groups', 
                    headers={ "Authorization": "Bearer " + self.token })

                if resp.status_code == 200:
                    data = resp.json()

                    existingData = self.dbManager.getItemGroups(cat['Id'])
                    deletedData = list(filter(lambda d: len(list(filter(lambda c: c['id'] == d['Id'], data))) == 0 ,existingData))
                    if deletedData and len(deletedData) > 0:
                        for dl in deletedData:
                            self.dbManager.deleteItemGroup(dl['Id'])

                    for d in data:
                        try:
                            respDetail = requests.get(self.apiUri + 'ItemGroup/' + str(d['id']),
                                headers={ "Authorization": "Bearer " + self.token })
                            if respDetail.status_code == 200:
                                detailObj = respDetail.json()
                                self.dbManager.saveItemGroup(detailObj)
                        except:
                            pass
        except Exception as e:
            pass


    def __updateMachineContent(self):
        try:
            resp = requests.get(self.apiUri + 'Machine/' + str(self.machineId),
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                self.dbManager.saveMachineContent(
                    {'rows': data['rows'], 
                    'cols': data['cols'], 
                    'spirals': data['spirals']})
        except:
            pass

    
    def __updateItems(self):
        try:
            categoryList = self.dbManager.getItemCategories()
            
            for cat in categoryList:
                resp = requests.get(self.apiUri + 'ItemCategory/' + str(cat['Id']) + '/Items',
                    headers={ "Authorization": "Bearer " + self.token })
                
                if resp.status_code == 200:
                    data = resp.json()

                    existingData = self.dbManager.getItemsByCategory(cat['Id'])
                    deletedData = list(filter(lambda d: len(list(filter(lambda c: c['id'] == d['Id'], data))) == 0 ,existingData))
                    if deletedData and len(deletedData) > 0:
                        for dl in deletedData:
                            self.dbManager.deleteItem(dl['Id'])

                    for d in data:
                        self.dbManager.saveItem(d)
        except Exception as e:
            pass


    def __updateSpirals(self):
        try:
            resp = requests.get(self.apiUri + 'Machine/' + str(self.machineId) + '/MachineSpiralContents',
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                self.dbManager.saveSpirals(data)
        except Exception as e:
            pass


    def sendSpiralConsuming(self, consumeInfo) -> bool:
        returnVal = False
        try:
            respDeliver = requests.post(self.apiUri + 'Machine/'+ str(self.machineId) +'/DeliverProduct', json={
                'employeeId': int(consumeInfo['employeeId']),
                'itemId': int(consumeInfo['itemId']),
                'spiralNo': int(consumeInfo['spiralNo']),
                'deliverDate': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            }, headers={ "Authorization": "Bearer " + self.token })
            if respDeliver.status_code == 200:
                returnVal = True
        except Exception as e:
            pass
        return returnVal


    def updateVideo(self):
        try:
            self.__obtainToken()
            overwrite = False

            with requests.get(self.apiUri + 'Machine/' + str(self.machineId) + '/Video',
                headers={ "Authorization": "Bearer " + self.token }, stream=True) as resp:
                if isfile('video/welcome.mp4') == False or (os.stat('video/welcome.mp4').st_size != len(resp.content)):
                    overwrite = True
                    with open('video/welcome_new.mp4', 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=8192): 
                            f.write(chunk)

                if overwrite == False and isfile('video/welcome.mp4') and isfile('video/welcome_new.mp4'):
                    if os.stat('video/welcome.mp4').st_size != os.stat('video/welcome_new.mp4').st_size:
                        os.remove('video/welcome.mp4') 
                        overwrite = True
                else:
                    overwrite = True

                if overwrite == True and isfile('video/welcome_new.mp4'):
                    os.rename('video/welcome_new.mp4', 'video/welcome.mp4')
                    self._backend.raiseNewVideoArrived()
                else:
                    try:
                        if isfile('video/welcome_new.mp4'):
                            os.remove('video/welcome_new.mp4')
                    except:
                        pass
        except Exception as e:
            print(e)
            pass


    def __runnerLoop(self):
        while self.mustRun:
            try:
                self.configData = self.dbManager.getMachineConfig()
                if self.configData:
                    self.apiUri = self.configData['ApiAddr']

                    # obtain api token
                    if len(self.token) == 0:
                        self.__obtainToken()

                    # update local data
                    self.__updateMachineContent()
                    self.__updateEmployees()
                    self.__updateItemCategories()
                    self.__updateItemGroups()
                    self.__updateItems()
                    self.__updateSpirals()
                    self.updateVideo()

                sleep(10)
            except:
                pass


    def stop(self):
        self.mustRun = False
        if self.runner:
            try:
                self.runner.stop()
                #self.runner.join()
            except:
                pass