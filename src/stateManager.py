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
        self.isCreditsVisible = True
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


    def loginByCard(self, cardNo):
        loginResult = {
            'result': False,
            'message': '',
        }

        self.__updateConfig()
        try:
            resp = requests.post(self.apiUri + 'User/LoginCard', json={
                'login': cardNo,
                'password': '',
                'dealerCode': self.configData['DealerCode'],
                'plantCode': self.configData['PlantCode'],
            }, timeout=15)

            if resp.status_code == 200:
                respObj = resp.json()

                if respObj['result'] == True:
                    self.token = respObj['token']
                    self.userData = respObj['employee']
                    loginResult['result'] = True
                else:
                    loginResult['result'] = False
                    loginResult['message'] = 'OKUTULAN KART BİLGİLERİ GEÇERSİZ'
            else:
                loginResult['result'] = False
                loginResult['message'] = 'OKUTULAN KART BİLGİLERİ GEÇERSİZ'
        except Exception as e:
            print(e)
            newConnErr = str(e).find('NewConnectionError') != -1
            if (e is requests.exceptions.ConnectionError or e is requests.exceptions.ConnectTimeout 
                or e is requests.exceptions.Timeout or e is requests.exceptions.URLRequired
                or e is requests.exceptions.TooManyRedirects or newConnErr):
                loginResult['result'] = False
                loginResult['message'] = 'SUNUCUYA ERİŞİM SAĞLANAMADI'
                
        return loginResult


    def logout(self):
        self.token = ''
        self.userData = {}