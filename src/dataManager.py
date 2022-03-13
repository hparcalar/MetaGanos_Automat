from distutils.command.config import config
import sqlite3
from sqlite3 import Error, connect
from src.dataMigrator import DataMigrator

class DataManager():
    def __init__(self):
        self.dbMigrator = DataMigrator()
        self.migrate()

    def migrate(self):
        self.connect()
        self.dbMigrator.migrate(self.connection)
        self.disconnect()

    def connect(self):
        try:
            self.connection = sqlite3.connect("data/mg.db")
        except Error as e:
            print(e)

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except:
            pass

    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # MACHINE BUSINESS
    def checkMachineConfig(self) -> bool:
        machineConfigExists = False
        self.connect()
        try:
            configRecord = self.connection.execute("SELECT * FROM MachineConfig").fetchone()
            if configRecord:
                machineConfigExists = True
        except:
            pass
        self.disconnect()
        return machineConfigExists

    def getMachineConfig(self):
        configData = None
        self.connect()
        try:
            configData = self.connection.execute("SELECT * FROM MachineConfig").fetchone()
        except:
            pass
        self.disconnect()

        if configData:
            return {
                'Code': configData[1],
                'Name': configData[2],
                'ApiAddr': configData[3],
                'ModbusType': configData[4],
                'ModbusServerAddr': configData[5],
                'ModbusServerPort': configData[6],
                'ModbusCoilPushItem': configData[7],
                'ModbusCoilServiceFlag': configData[8],
                'ModbusRegisterSpiralNo': configData[9],
                'Rows': configData[10],
                'Cols': configData[11]
            }
        return configData
    
    def saveMachineContent(self, content) -> bool:
        saveResult = False
        self.connect()

        try:
            self.connection.execute("UPDATE MachineConfig SET Rows=" + str(content['rows'])
                + ", Cols=" + str(content['cols']))

            # if content['spirals'] and len(content['spirals']) > 0:
            #     self.connection.execute("DELETE FROM Spiral")
            #     for spr in content['spirals']:
            #         self.connection.execute("INSERT INTO Spiral(SpiralNo, ItemCategoryId, ItemId, ActiveQuantity)"
            #             + " VALUES("+ str(spr['posOrders']) +", "+ (str(spr['itemCategoryId']) if spr['itemCategoryId'] else "NULL")
            #              +", "+ (str(spr['itemId']) if spr['itemId'] else "NULL") +", "
            #              + (str(int(spr['activeQuantity'])) if spr['activeQuantity'] else "NULL") +")")

            self.connection.commit()
            saveResult = True
        except Exception as e:
            pass

        self.disconnect()
        return saveResult

    def saveMachineConfig(self, config) -> bool:
        saveResult = False
        self.connect()

        try:
            existingRecord = self.connection.execute("SELECT * FROM MachineConfig").fetchone()
            if existingRecord is None:
                self.connection.execute("""
                    INSERT INTO MachineConfig(Id,Code, ApiAddr,ModbusType,ModbusServerAddr,ModbusServerPort,ModbusCoilPushItem,ModbusCoilServiceFlag,
                        ModbusRegisterSpiralNo)
                    VALUES (1,'"""+ config['machineCode'] +"""', '"""+ config['apiAddr'] +"""','"""+ config['modbusType'] +"""',
                    '"""+ config['modbusServerAddr'] +"""',
                        '"""+ config['modbusServerPort'] +"""', '"""+ config['modbusCoilPushItem'] +"""', 
                        '"""+ config['modbusCoilServiceFlag'] +"""',
                        '"""+ config['modbusRegisterSpiralNo'] +"""')
                """)
            else:
                self.connection.execute("""
                    UPDATE MachineConfig SET Code='"""+ config['machineCode'] +"""', ApiAddr='"""+ config['apiAddr'] +"""',
                        ModbusType='"""+ config['modbusType'] +"""', ModbusServerAddr='"""+config['modbusServerAddr']+"""',
                        ModbusServerPort='"""+config['modbusServerPort']+"""', ModbusCoilPushItem='"""+config['modbusCoilPushItem']+"""',
                        ModbusCoilServiceFlag='"""+config['modbusCoilServiceFlag']+"""', 
                        ModbusRegisterSpiralNo='"""+config['modbusRegisterSpiralNo']+"""'
                """)

            self.connection.commit()
        except:
            pass

        saveResult = True
        self.disconnect()
        return saveResult

    # EMPLOYEE BUSINESS
    def saveEmployee(self, employee) -> bool:
        returnVal = False
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM Employee WHERE Id = """ + str(employee['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO Employee(Id, EmployeeCode, EmployeeName, CardNo, CardHexNo, DepartmentName)
                        VALUES("""+ str(employee['id']) +""", '""" + employee['employeeCode'] + """',
                        '"""+ employee['employeeName'] +"""', '"""+ employee['employeeCardCode'] +"""', '',
                        '"""+ employee['departmentName'] +"""')
                    """)
            else:
                self.connection.execute("""
                        UPDATE Employee SET EmployeeCode='"""+ employee['employeeCode'] +"""',
                            EmployeeName='"""+ employee['employeeName'] +"""',
                            CardNo='"""+ employee['employeeCardCode'] +"""',
                            DepartmentName='"""+employee['departmentName']+"""' WHERE Id="""+ str(employee['id']) +"""
                    """)

            self.connection.commit()
            returnVal = True
        except Exception as e:
            pass
        self.disconnect()
        return returnVal


    # ITEM CATEGORY BUSINESS
    def saveItemCategory(self, category):
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM ItemCategory WHERE Id = """ + str(category['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO ItemCategory(Id, ItemCategoryCode, ItemCategoryName, CategoryImage)
                        VALUES("""+ str(category['id']) +""", '""" + category['itemCategoryCode'] + """',
                        '"""+ category['itemCategoryName'] +"""', '"""+ category['categoryImage'] +"""')""")
            else:
                self.connection.execute("""
                        UPDATE ItemCategory SET ItemCategoryCode='"""+ category['itemCategoryCode'] +"""',
                            ItemCategoryName='"""+ category['itemCategoryName'] +"""',
                            CategoryImage='"""+ category['categoryImage'] +"""' WHERE Id="""+ str(category['id']) +"""
                    """)

            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()

    
    def getItemCategory(self, categoryId):
        returnData = None
        self.connect()
        try:
            r = self.connection.execute("SELECT * FROM ItemCategory WHERE Id=" + str(categoryId)).fetchone()
            returnData = {
                    'Id': r[0],
                    'ItemCategoryCode': r[1],
                    'ItemCategoryName': r[2],
                    'CategoryImage': r[3]
                }
        except:
            pass
        self.disconnect()
        return returnData


    def getItemCategories(self):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM ItemCategory").fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemCategoryCode': r[1],
                    'ItemCategoryName': r[2],
                    'CategoryImage': r[3]
                })
        except:
            pass
        self.disconnect()
        return returnData

    # ITEM GROUP BUSINESS
    def saveItemGroup(self, group):
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM ItemGroup WHERE Id = """ + str(group['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO ItemGroup(Id, ItemGroupCode, ItemGroupName, ItemCategoryId)
                        VALUES("""+ str(group['id']) +""", '""" + group['itemGroupCode'] + """',
                        '"""+ group['itemGroupName'] +"""', """+ str(group['itemCategoryId']) +""")""")
            else:
                self.connection.execute("""
                        UPDATE ItemGroup SET ItemGroupCode='"""+ group['itemGroupCode'] +"""',
                            ItemGroupName='"""+ group['itemGroupName'] +"""',
                            ItemCategoryId="""+ str(group['itemCategoryId']) +""" WHERE Id="""+ str(group['id']) +"""
                    """)

            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()


    def getItemGroup(self, groupId):
        returnData = None
        self.connect()
        try:
            r = self.connection.execute("SELECT * FROM ItemGroup WHERE Id=" + str(groupId)).fetchone()
            returnData = {
                    'Id': r[0],
                    'ItemGroupCode': r[1],
                    'ItemGroupName': r[2],
                    'ItemCategoryId': r[4]
                }
        except:
            pass
        self.disconnect()
        return returnData


    def getItemGroups(self, categoryId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM ItemGroup WHERE ItemCategoryId=" + str(categoryId)).fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemGroupCode': r[1],
                    'ItemGroupName': r[2],
                    'ItemCategoryId': r[4]
                })
        except:
            pass
        self.disconnect()
        return returnData

    # ITEM BUSINESS
    def saveItem(self, item):
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM Item WHERE Id = """ + str(item['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO Item(Id, ItemCode, ItemName, ItemCategoryId, ItemGroupId)
                        VALUES("""+ str(item['id']) +""", '""" + item['itemCode'] + """',
                        '"""+ item['itemName'] +"""', """+ str(item['itemCategoryId']) +""", """+ str(item['itemGroupId']) +""")""")
            else:
                self.connection.execute("""
                        UPDATE Item SET ItemCode='"""+ item['itemCode'] +"""',
                            ItemName='"""+ item['itemName'] +"""',
                            ItemCategoryId="""+ str(item['itemCategoryId']) +""", ItemGroupId="""+ str(item['itemGroupId']) 
                            +""" WHERE Id="""+ str(item['id']) +"""
                    """)

            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()

    
    def getItems(self, groupId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Item WHERE ItemGroupId=" + str(groupId)).fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemCode': r[1],
                    'ItemName': r[2],
                    'ItemGroupId': r[3],
                    'ItemCategoryId': r[4]
                })
        except:
            pass
        self.disconnect()
        return returnData

    
    def getItem(self, itemId):
        returnData = None
        self.connect()
        try:
            r = self.connection.execute("SELECT * FROM Item WHERE Id=" + str(itemId)).fetchone()
            returnData = {
                    'Id': r[0],
                    'ItemCode': r[1],
                    'ItemName': r[2],
                    'ItemGroupId': r[3],
                    'ItemCategoryId': r[4]
                }
        except:
            pass
        self.disconnect()
        return returnData

    
    # SPIRAL BUSINESS
    def saveSpirals(self, spirals):
        self.connect()
        try:
            self.connection.execute("DELETE FROM Spiral")
            for item in spirals:
                self.connection.execute("""
                        INSERT INTO Spiral(Id, SpiralNo, ItemCategoryId, ItemId, ActiveQuantity)
                        VALUES("""+ str(item['id']) +""", '""" + str(item['posOrders']) + """',
                        """+ str(item['itemCategoryId']) +""", """+ str(item['itemId']) +""", """+ str(item['activeQuantity']) +""")""")
            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()

    def getSpiralInfo(self, spiralNo):
        returnData = None
        self.connect()
        try:
            r = self.connection.execute("SELECT ItemCategoryId, ItemId FROM Spiral WHERE SpiralNo = " + str(spiralNo)).fetchone()
            if r:
                returnData = {
                    "ItemCategoryId": r[0],
                    "ItemId": r[1]
                }
        except Exception as e:
            pass
        self.disconnect()
        return returnData

    def getProperSpirals(self, itemId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Spiral WHERE ItemId = " + str(itemId)).fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'SpiralNo': r[1],
                    'ItemCategoryId': r[2],
                    'ItemId': r[3],
                    'ActiveQuantity': r[4]
                })
        except Exception as e:
            pass
        self.disconnect()
        return returnData


    # EMPLOYEE RIGHTS BUSINESS
    def saveCredits(self, employeeId, credits):
        self.connect()
        try:
            self.connection.execute("DELETE FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId))
            for item in credits:
                self.connection.execute("""
                        INSERT INTO EmployeeCredit(Id, EmployeeId, ItemCategoryId, ItemGroupId, ItemId, ActiveCredit)
                        VALUES("""+ str(item['id']) +""", """ + str(item['employeeId']) + """,
                        """+ str(item['itemCategoryId']) +""", NULL, NULL, """+ str(item['activeCredit']) +""")""")
            self.connection.commit()
        except Exception as e:
            print(e)
            pass
        self.disconnect()


    def getCreditInfo(self, employeeId, itemCategoryId):
        returnData = {
            "ActiveCredit": 0
        }

        self.connect()
        try:
            r = self.connection.execute("SELECT ActiveCredit FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId) 
                + " AND ItemCategoryId = " + str(itemCategoryId)).fetchone()
            if r and int(r[0]) > 0:
                returnData['ActiveCredit'] = int(r[0])
        except Exception as e:
            pass
        self.disconnect()

        return returnData

    
    def checkEmployeeHasCredit(self, employeeId, itemCategoryId) -> bool:
        hasCredit = False
        self.connect()
        try:
            r = self.connection.execute("SELECT ActiveCredit FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId) 
                + " AND ItemCategoryId = " + str(itemCategoryId)).fetchone()
            if r and int(r[0]) > 0:
                hasCredit = True
        except Exception as e:
            pass
        self.disconnect()
        return hasCredit


    def consumeCredit(self, employeeId, itemCategoryId, syncStatus) -> bool:
        consumeResult = False
        self.connect()
        try:
            self.connection.execute("UPDATE EmployeeCredit SET ActiveCredit = ActiveCredit - 1 WHERE EmployeeId = " + str(employeeId) 
                + " AND ItemCategoryId = " + str(itemCategoryId))
            self.connection.execute("INSERT INTO CreditConsuming(EmployeeId, ItemCategoryId, Credit, SyncStatus)"
                + " VALUES("+ str(employeeId) +", "+ str(itemCategoryId) +", 1, "+ str(syncStatus) +")")
            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()
        return consumeResult


    def getWaitingConsumingsForSync(self):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT Id, EmployeeId, ItemCategoryId, Credit FROM CreditConsuming WHERE SyncStatus = 0").fetchall()
            for r in rows:
                returnData.append({
                    "Id": r[0],
                    "EmployeeId": r[1],
                    "ItemCategoryId": r[2],
                    "Credit": r[3]
                })
        except Exception as e:
            pass
        self.disconnect()
        return returnData

    
    def setConsumingAsSynced(self, consumingId):
        self.connect()
        try:
            self.connection.execute("UPDATE CreditConsuming SET SyncStatus = 1 WHERE Id = " + str(consumingId))
            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()