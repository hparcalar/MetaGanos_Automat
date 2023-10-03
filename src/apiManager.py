from src.dataManager import DataManager
from threading import Thread
from src.hkThread import HekaThread
from time import sleep
from datetime import datetime
from os.path import isfile, getmtime
import os
import json
import requests
import datetime

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
        self.creditsData = []
        self.lastUpdateDate = datetime.datetime.min
        self.runner = HekaThread(target=self.__runnerLoop)


    def listen(self):
        self.mustRun = True
        self.runner.start()

    
    def getItemCategories(self):
        resultData = []
        try:
            # self.__obtainToken()

            plantId = None
            respFindPlant = requests.get(self.apiUri + 'Plant/Find/' + self.dealerCode + '/' + self.plantCode,
                headers={ "Authorization": "Bearer " + self.token })
            if respFindPlant.status_code == 200:
                data = respFindPlant.json()
                plantId = data['id']

            if plantId:
                resp = requests.get(self.apiUri + 'Plant/' + str(plantId) + '/ItemCategoriesNonWr', 
                    headers={ "Authorization": "Bearer " + self.token })

                if resp.status_code == 200:
                    dataCats = resp.json()
                    creditList = self.creditsData

                    dataCats = list(filter(lambda d: len(list(filter(lambda x: int(x['itemCategoryId']) == int(d['id']), creditList))) > 0, dataCats))

                    # for d in dataCats:
                    #     try:
                    #         respDetail = requests.get(self.apiUri + 'ItemCategory/' + str(d['id']), 
                    #             headers={ "Authorization": "Bearer " + self.token })
                    #         if respDetail.status_code == 200:
                    #             detailObj = respDetail.json()
                    #             d['categoryImage'] = detailObj['categoryImage']
                    #     except:
                    #         pass

                    resultData = dataCats
        except Exception as e:
            pass

        return resultData

    
    def getItemGroups(self, itemCategoryId):
        resultData = {
            'categoryName': '',
            'groups': []
        }
        try:
            self.__obtainToken()

            catName = ''

            respCat = requests.get(self.apiUri + 'ItemCategory/' + str(itemCategoryId), 
                    headers={ "Authorization": "Bearer " + self.token })
            if respCat.status_code == 200:
                catName = respCat.json()['itemCategoryName']

            resp = requests.get(self.apiUri + 'ItemCategory/' + str(itemCategoryId) + '/GroupsNonWr', 
                    headers={ "Authorization": "Bearer " + self.token })

            if resp.status_code == 200:
                data = resp.json()

                creditList = self.creditsData
                data = list(filter(lambda d: len(list(filter(lambda x: x['itemGroupId'] != None and int(x['itemGroupId']) == int(d['id']) 
                    or (int(x['itemCategoryId']) == int(itemCategoryId) and x['itemGroupId'] == None), creditList))) > 0, data))

                # for d in data:
                #     try:
                #         respDetail = requests.get(self.apiUri + 'ItemGroup/' + str(d['id']),
                #             headers={ "Authorization": "Bearer " + self.token })
                #         if respDetail.status_code == 200:
                #             detailObj = respDetail.json()
                #             d['groupImage'] = detailObj['groupImage']
                #     except:
                #         pass
                
                resultData['categoryName'] = catName
                resultData['groups'] = data
        except:
            pass
        return resultData


    def getItems(self, itemCategoryId, itemGroupId):
        resultData = {
            'groupName' : '',
            'items': []
        }
        try:
            self.__obtainToken()

            grName = ''

            respGr= requests.get(self.apiUri + 'ItemGroup/' + str(itemGroupId), 
                    headers={ "Authorization": "Bearer " + self.token })
            if respGr.status_code == 200:
                grName = respGr.json()['itemGroupName']

            resp = requests.get(self.apiUri + 'ItemGroup/' + str(itemGroupId) + '/ItemsNonWr',
                    headers={ "Authorization": "Bearer " + self.token })
                
            if resp.status_code == 200:
                data = resp.json()
                creditList = self.creditsData
                data = list(filter(lambda d: len(list(filter(lambda x: (x['itemId'] != None and int(x['itemId']) == int(d['id']))
                    or (int(x['itemCategoryId']) == int(itemCategoryId) and x['itemGroupId'] == None and x['itemId'] == None)
                    or (x['itemGroupId'] != None and int(x['itemGroupId']) == itemGroupId and x['itemId'] == None), creditList))) > 0, data))

                # for d in data:
                #     try:
                #         respDetail = requests.get(self.apiUri + 'Item/' + str(d['id']),
                #             headers={ "Authorization": "Bearer " + self.token })
                #         if respDetail.status_code == 200:
                #             detailObj = respDetail.json()
                #             d['itemImage'] = detailObj['itemImage']
                #     except:
                #         pass
                # print(data)
                resultData['groupName'] = grName
                resultData['items'] = data
        except Exception as e: print(e)
        return resultData


    def getSpirals(self, itemId):
        resultData = {
            'itemName' : '',
            'spirals': []
        }
        try:
            self.__obtainToken()

            itemName = ''

            respItem= requests.get(self.apiUri + 'Item/' + str(itemId), 
                    headers={ "Authorization": "Bearer " + self.token })
            if respItem.status_code == 200:
                itemName = respItem.json()['itemName']

            resp = requests.get(self.apiUri + 'Machine/' + str(self.machineId) + '/MachineSpiralContents',
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()

            resultData['itemName'] = itemName
            resultData['spirals'] = data
        except:
            pass
        return resultData


    def fetchCredits(self, employeeId):
        try:
            self.__obtainToken()

            resp = requests.get(self.apiUri + 'Employee/' + str(employeeId) + '/FetchCredits',
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                self.creditsData = data
        except: pass


    def checkCredits(self, consumeInfo):
        returnVal = [False,""]
        try:
            respDeliver = requests.post(self.apiUri + 'Machine/'+ str(self.machineId) +'/CheckCreditsForDelivery', json={
                'employeeId': int(consumeInfo['employeeId']),
                'itemId': int(consumeInfo['itemId']),
                'spiralNo': int(consumeInfo['spiralNo']),
                'deliverDate': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            }, headers={ "Authorization": "Bearer " + self.token })
            if respDeliver.status_code == 200:
                data = respDeliver.json()
                returnVal[0] = data['result']
                returnVal[1] = data['errorMessage']
        except Exception as e:
            pass
        return returnVal


    def getCreditInfo(self, employeeId, itemCategoryId, itemGroupId = None, itemId = None):
        returnData = {
            "ActiveCredit": 0,
            "RangeType": 4,
            "RangeLength": 1,
            "CreditByRange": 0,
        }

        try:
            r = None
            if itemId:
                r = list(filter(lambda d: d['itemId'] == itemId 
                or (d['itemGroupId'] == itemGroupId and d['itemId'] == None) 
                or (d['itemCategoryId'] == itemCategoryId and d['itemId'] == None and d['itemGroupId'] == None),self.creditsData))[0]
            elif itemGroupId:
                r = list(filter(lambda d: d['itemGroupId'] == itemGroupId 
                or (d['itemCategoryId'] == itemCategoryId and d['itemGroupId'] == None),self.creditsData))[0]
            else:
                 r = list(filter(lambda d: d['itemCategoryId'] == itemCategoryId,self.creditsData))[0]

            if r:
                returnData['ActiveCredit'] = int(r['rangeCredit'])
                returnData['RangeType'] = (int(r['rangeType']) if r['rangeType'] else 4)
                returnData['RangeLength'] = (int(r['rangeLength']) if r['rangeLength'] else 1)
                returnData['CreditByRange'] = (int(r['creditByRange']) if r['creditByRange'] else 0)
        except:
            pass

        return returnData


    def __obtainToken(self):
        try:
            self.configData = self.dbManager.getMachineConfig()
            if self.configData:
                self.apiUri = self.configData['ApiAddr']

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
                        print(str(d['employeeName']))
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
                resp = requests.get(self.apiUri + 'Plant/' + str(plantId) + '/ItemCategoriesNonWr', 
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
                resp = requests.get(self.apiUri + 'ItemCategory/' + str(cat['Id']) + '/GroupsNonWr', 
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
                resp = requests.get(self.apiUri + 'ItemCategory/' + str(cat['Id']) + '/ItemsNonWr',
                    headers={ "Authorization": "Bearer " + self.token })
                
                if resp.status_code == 200:
                    data = resp.json()

                    existingData = self.dbManager.getItemsByCategory(cat['Id'])
                    deletedData = list(filter(lambda d: len(list(filter(lambda c: c['id'] == d['Id'], data))) == 0 ,existingData))
                    if deletedData and len(deletedData) > 0:
                        for dl in deletedData:
                            self.dbManager.deleteItem(dl['Id'])

                    for d in data:
                        try:
                            respDetail = requests.get(self.apiUri + 'Item/' + str(d['id']),
                                headers={ "Authorization": "Bearer " + self.token })
                            if respDetail.status_code == 200:
                                detailObj = respDetail.json()
                                self.dbManager.saveItem(detailObj)
                        except:
                            pass
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

    def getMachineInfo(self):
        machineData = {
            'Rows': 0,
            'Cols': 0,
        }
        try:
            resp = requests.get(self.apiUri + 'Machine/' + str(self.machineId),
                headers={ "Authorization": "Bearer " + self.token })
            
            if resp.status_code == 200:
                data = resp.json()
                machineData['Rows'] = data['rows']
                machineData['Cols'] = data['cols']
        except Exception as e:
            pass
        return machineData


    def sendSpiralConsuming(self, consumeInfo) -> bool:
        returnVal = False
        try:
            respDeliver = requests.post(self.apiUri + 'Machine/'+ str(self.machineId) +'/DeliverProduct', json={
                'employeeId': int(consumeInfo['employeeId']),
                'itemId': int(consumeInfo['itemId']),
                'spiralNo': int(consumeInfo['spiralNo']),
                'deliverDate': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
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

                if isfile('video/welcome.mp4') and isfile('video/welcome_new.mp4'):
                    if os.stat('video/welcome.mp4').st_size != os.stat('video/welcome_new.mp4').st_size:
                        self._backend.raiseNewVideoArrived()
                        sleep(2)
                        os.remove('video/welcome.mp4') 
                        overwrite = True
                else:
                    overwrite = True

                if overwrite == True and isfile('video/welcome_new.mp4'):
                    os.rename('video/welcome_new.mp4', 'video/welcome.mp4')
                    self._backend.raiseStartNewVideo()
                else:
                    try:
                        if isfile('video/welcome_new.mp4'):
                            os.remove('video/welcome_new.mp4')
                    except:
                        pass
        except Exception as e:
            print(e)
            pass


    def __checkLastUpdate(self) -> bool:
        try:
            if self.lastUpdateDate == None:
                return True

            resp = requests.get(self.apiUri + 'Plant/LastUpdate/' + self.configData['DealerCode'] + '/' + self.configData['PlantCode'],
                    headers={ "Authorization": "Bearer " + self.token })
            if resp.status_code == 200:
                data = resp.text
                if len(data) > 0:
                    serverDate = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                    if serverDate > self.lastUpdateDate:
                        return True

            return False
        except Exception as e:
            print(e)
            return False
    

    def __runnerLoop(self):
        while self.mustRun:
            try:
                self.configData = self.dbManager.getMachineConfig()
                if self.configData:
                    self.apiUri = self.configData['ApiAddr']

                    # obtain api token
                    # if len(self.token) == 0:
                    self.__obtainToken()

                    if self.__checkLastUpdate() == True:
                        self.lastUpdateDate = datetime.datetime.now()
                        # update local data
                        # print("up mac")
                        # self.__updateMachineContent()
                        # print("up emp")
                        # self.__updateEmployees()
                        # print("up cat")
                        # self.__updateItemCategories()
                        # print("up gr")
                        # self.__updateItemGroups()
                        # print("up itm")
                        # self.__updateItems()
                        # print("up spr")
                        # self.__updateSpirals()
                        # print("up end")
                        thr = HekaThread(target=self.updateVideo)
                        thr.start()

                sleep(35)
            except Exception as e:
                print(e)
                pass


    def stop(self):
        self.mustRun = False
        if self.runner:
            try:
                self.runner.stop()
                #self.runner.join()
            except:
                pass