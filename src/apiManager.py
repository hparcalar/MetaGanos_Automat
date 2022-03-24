from src.dataManager import DataManager
from threading import Thread
from time import sleep
from datetime import datetime
import json
import requests

class ApiManager():
    def __init__(self):
        self.dbManager = DataManager()
        self.mustRun = False
        self.apiUri = ''
        self.token = ''
        self.configData = {}
        self.runner = Thread(target=self.__runnerLoop)


    def listen(self):
        self.mustRun = True
        self.runner.start()


    def __obtainToken(self):
        try:
            resp = requests.post(self.apiUri + 'User/LoginMachine', json={
                'login': self.configData['Code'],
                'password': ''
            })

            if resp.status_code == 200:
                self.token = resp.text
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
            resp = requests.get(self.apiUri + 'ItemCategory', 
                headers={ "Authorization": "Bearer " + self.token })

            if resp.status_code == 200:
                data = resp.json()
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
            pass

    
    def __updateItemGroups(self):
        try:
            resp = requests.get(self.apiUri + 'ItemGroup', 
                headers={ "Authorization": "Bearer " + self.token })

            if resp.status_code == 200:
                data = resp.json()
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
            resp = requests.get(self.apiUri + 'Machine/Find/' + self.configData['Code'],
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
            resp = requests.get(self.apiUri + 'Item/ForMachine/' + self.configData['Code'],
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                for d in data:
                    self.dbManager.saveItem(d)
        except Exception as e:
            pass


    def __updateSpirals(self):
        try:
            resp = requests.get(self.apiUri + 'Machine/' + self.configData['Code'] + '/SpiralContents',
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                self.dbManager.saveSpirals(data)
        except Exception as e:
            pass


    def sendSpiralConsuming(self, consumeInfo) -> bool:
        returnVal = False
        try:
            resp = requests.get(self.apiUri + 'Machine/Find/' + self.configData['Code'],
                headers={ "Authorization": "Bearer " + self.token })
            if resp.status_code == 200:
                macData = resp.json()
                if int(macData['id']) > 0:
                    prm = {
                        'employeeId': int(consumeInfo['employeeId']),
                        'itemId': int(consumeInfo['itemId']),
                        'spiralNo': int(consumeInfo['spiralNo']),
                        'deliverDate': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    respDeliver = requests.post(self.apiUri + 'Machine/'+ str(macData['id']) +'/DeliverProduct', json={
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

                sleep(10)
            except:
                pass

    def stop(self):
        self.mustRun = False
        if self.runner:
            try:
                self.runner.join()
            except:
                pass