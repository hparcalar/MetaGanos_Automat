from src.dataManager import DataManager
import requests

class StateManager():
    def __init__(self):
        self.dbManager = DataManager()
        self.apiUri = ''
        self.token = ''
        self.selectedCategoryId = None
        self.selectedGroupId = None
        self.selectedItemId = None
        self.pushProcessFinished = True
        self.userData = {}
        self.configData = {}


    def __updateConfig(self):
        try:
            self.configData = self.dbManager.getMachineConfig()
            self.apiUri = self.configData['ApiAddr']
        except Exception as e:
            print(e)

    
    def getUserData(self):
        return self.userData


    def loginByCard(self, cardNo) -> bool:
        self.__updateConfig()
        try:
            resp = requests.post(self.apiUri + 'User/LoginCard', json={
                'login': cardNo,
                'password': '',
                'dealerCode': self.configData['DealerCode'],
                'plantCode': self.configData['PlantCode'],
            })

            if resp.status_code == 200:
                respObj = resp.json()

                if respObj['result'] == True:
                    self.token = respObj['token']
                    self.userData = respObj['employee']
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False


    def logout(self):
        self.token = ''
        self.userData = {}