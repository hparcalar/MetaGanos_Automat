from threading import Thread
from src.hkThread import HekaThread
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from src.dataManager import DataManager
from time import sleep


class ModbusManager():
    def __init__(self, handler):
        self.dbManager = DataManager()
        self.configData = None
        self.handler = handler
        self.serviceFlagActive = False
        self.threadUpdater = None
        self.threadListener = None
        self.runUpdater = False
        self.runListener = False
        self.__start()


    def __start(self):
        self.runUpdater = True
        #self.runListener = True
        self.threadUpdater = HekaThread(target=self.__updateLoop)
        #self.threadListener = Thread(target=self.__listenerLoop)
        self.threadUpdater.start()
        #self.threadListener.start()


    def stop(self):
        self.runUpdater = False
        self.runListener = False
        if self.threadUpdater:
            try:
                self.threadUpdater.stop()
                # self.threadUpdater.join()
            except:
                pass
            try:
                self.threadListener.join()
            except:
                pass


    def pushItem(self, spiralNo) -> bool:
        pushResult = { 'Result': False, 'ErrorMessage': '' }
        # pushResult['Result'] = True
        # return pushResult

        try:
            client = None
            if self.configData['ModbusType'] == "TCP":
                client = ModbusTcpClient(self.configData['ModbusServerAddr'])
                
            elif self.configData['ModbusType'] == "RTU":
                client = ModbusSerialClient(method='rtu', port=self.configData['ModbusServerAddr'], baudrate=9600, timeout=1)
                client.connect()
            
            # check is ready bit
            # waitingForReady = 0
            # while self.__readCoils(client, 35) == False:
            #     sleep(0.5)
            #     waitingForReady = waitingForReady + 0.5
            #     if waitingForReady >= 4:
            #         return False

            # empty drop sensor flag
            self.__writeCoils(client, 37, [0])

            # pick spiral
            self.__writeRegisters(client, int(spiralNo))

            # move arm
            # self.__writeCoils(client, 31, [1]) # is working bit launches True (36)
            # sleep(1)
            # self.__writeCoils(client, 31, [0])

            # check bussy bit
            # while self.__readCoils(client, 33) == True:
            #     sleep(0.5)

            # move circle
            self.__writeCoils(client, 16, [1]) 
            sleep(1)
            self.__writeCoils(client, 16, [0])

            # bussy bit
            # while self.__readCoils(client, 34) == True:
            #     sleep(0.5)

            # move home
            # self.__writeCoils(client, 32, [1])
            # sleep(1)
            # self.__writeCoils(client, 32, [0]) # is working bit False (36)

            # check drop sensor
            sleep(4)
            dropResult = self.__readCoils(client, 37)

            if dropResult == False:
                self.__writeCoils(client, 38, [1])
                sleep(2)
                dropResult = self.__readCoils(client, 37)

            client.close()
            pushResult['Result'] = dropResult

            if dropResult == False:
                pushResult['ErrorMessage'] = 'Ürün verilemedi, krediniz kartınıza iade edildi.'
        except Exception as e:
            pushResult['Result'] = False
            pushResult['ErrorMessage'] = 'Cihaz iletişiminde bir hata oluştu. Lütfen daha sonra tekrar deneyiniz.'

        return pushResult
    

    def __writeRegisters(self, client, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Little, wordorder=Endian.Little)
        builder.add_32bit_uint(value)
        registers = builder.to_registers()

        nReg = []
        for rg in registers:
            nReg.append(int(rg / 256))

        result = client.write_registers(2065, nReg, skip_encode=False, unit=1)


    def __writeCoils(self, client, coilNo, value):
        result = client.write_coils(coilNo, value)


    def __readCoils(self, client, coilNo) -> bool:
        result = client.read_coils(coilNo, 1)
        return result.bits[0]

    
    def __getConfig(self):
        self.configData = self.dbManager.getMachineConfig()


    def __updateLoop(self):
        while self.runUpdater:
            self.__getConfig()
            sleep(3)
    

    def __listenerLoop(self):
        while self.runListener:
            try:
                if self.configData['ModbusType'] == "TCP":
                    client = ModbusTcpClient(self.configData['ModbusServerAddr'])
                    # read coils for service flag
                    if self.configData['ModbusCoilServiceFlag']:
                        result = client.read_coils(int(self.configData['ModbusCoilServiceFlag']),1)
                        if result.bits[0] == True and self.serviceFlagActive == False:
                            self.serviceFlagActive = True
                            if self.handler:
                                self.handler.onServiceFlagActivated()
                        elif result.bits[0] == False:
                            self.serviceFlagActive = False
                    client.close()
                elif self.configData['ModbusType'] == "RTU":
                    client = ModbusSerialClient(method='rtu', port=self.configData['ModbusServerAddr'], baudrate=9600, timeout=1)
                    client.connect()
                    # read coils for service flag
                    if self.configData['ModbusCoilServiceFlag']:
                        result = client.read_coils(int(self.configData['ModbusCoilServiceFlag']),1)
                        if result.bits[0] == True and self.serviceFlagActive == False:
                            self.serviceFlagActive = True
                            if self.handler:
                                self.handler.onServiceFlagActivated()
                        elif result.bits[0] == False:
                            self.serviceFlagActive = False
                    client.close()
                    pass
            except:
                pass

            sleep(3)