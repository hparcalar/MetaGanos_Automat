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
        connected = False

        try:
            self.connection.cursor()
            connected = True
        except:
            connected = False

        if connected == False:
            try:
                self.connection = sqlite3.connect("data/mg.db")
            except Error as e:
                pass

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
        except Exception as e:
            print(e)
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
                'Cols': configData[11],
                'DealerCode': configData[12],
                'PlantCode': configData[13],
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
            config['modbusServerPort'] = ''
            config['modbusCoilPushItem'] = ''
            config['modbusCoilServiceFlag'] = ''
            config['modbusRegisterSpiralNo'] = ''

            existingRecord = self.connection.execute("SELECT * FROM MachineConfig").fetchone()
            if existingRecord is None:
                self.connection.execute("""
                    INSERT INTO MachineConfig(Id,Code, ApiAddr,ModbusType,ModbusServerAddr,ModbusServerPort,ModbusCoilPushItem,ModbusCoilServiceFlag,
                        ModbusRegisterSpiralNo, DealerCode, PlantCode)
                    VALUES (1,'"""+ config['machineCode'] +"""', '"""+ config['apiAddr'] +"""','"""+ config['modbusType'] +"""',
                    '"""+ config['modbusServerAddr'] +"""',
                        '"""+ config['modbusServerPort'] +"""', '"""+ config['modbusCoilPushItem'] +"""', 
                        '"""+ config['modbusCoilServiceFlag'] +"""',
                        '"""+ config['modbusRegisterSpiralNo'] +"""', 
                        '"""+ config['dealerCode'] +"""',
                        '"""+ config['plantCode'] +"""'
                        )
                """)
            else:
                self.connection.execute("""
                    UPDATE MachineConfig SET Code='"""+ config['machineCode'] +"""', ApiAddr='"""+ config['apiAddr'] +"""',
                        ModbusType='"""+ config['modbusType'] +"""', ModbusServerAddr='"""+config['modbusServerAddr']+"""',
                        ModbusServerPort='"""+config['modbusServerPort']+"""', ModbusCoilPushItem='"""+config['modbusCoilPushItem']+"""',
                        ModbusCoilServiceFlag='"""+config['modbusCoilServiceFlag']+"""', 
                        ModbusRegisterSpiralNo='"""+config['modbusRegisterSpiralNo']+"""', DealerCode='"""+ config['dealerCode'] +"""', PlantCode='"""+ config['plantCode'] +"""'
                """)

            self.connection.commit()
        except Exception as e:
            print(e)

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
                        INSERT INTO ItemCategory(Id, ItemCategoryCode, ItemCategoryName, CategoryImage, CreditRangeType, CreditByRange)
                        VALUES("""+ str(category['id']) +""", '""" + category['itemCategoryCode'] + """',
                        '"""+ category['itemCategoryName'] +"""', '"""+ category['categoryImage'] +"""', 
                            """+ (str(category['creditRangeType']) if category['creditRangeType'] else 'NULL') +""", 
                            """+ (str(category['creditByRange']) if category['creditByRange'] else 'NULL') +""")""")
            else:
                self.connection.execute("""
                        UPDATE ItemCategory SET ItemCategoryCode='"""+ category['itemCategoryCode'] +"""',
                            ItemCategoryName='"""+ category['itemCategoryName'] +"""',
                            CategoryImage='"""+ category['categoryImage'] +"""',
                            CreditRangeType="""+ (str(category['creditRangeType']) if category['creditRangeType'] else 'NULL') +""",
                            CreditByRange= """+ (str(category['creditByRange']) if category['creditByRange'] else 'NULL') +""" 
                            WHERE Id="""+ str(category['id']) +"""
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
                    'CategoryImage': r[3],
                    'CreditRangeType': r[4],
                    'CreditByRange': r[5],
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
                    'CategoryImage': r[3],
                    'CreditRangeType': r[4],
                    'CreditByRange': r[5],
                })
        except:
            pass
        self.disconnect()
        return returnData

    def getProperItemCategories(self, employeeId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM ItemCategory AS ic "
                " WHERE EXISTS(SELECT * FROM EmployeeCredit AS cr WHERE cr.EmployeeId = "+ str(employeeId) 
                +" AND cr.ItemCategoryId = ic.Id)").fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemCategoryCode': r[1],
                    'ItemCategoryName': r[2],
                    'CategoryImage': r[3],
                    'CreditRangeType': r[4],
                    'CreditByRange': r[5],
                })
        except:
            pass
        self.disconnect()
        return returnData

    def deleteItemCategory(self, categoryId):
        self.connect()
        try:
            groupsOfCat = self.getItemGroups(categoryId, False)
            if groupsOfCat and len(groupsOfCat) > 0:
                for gr in groupsOfCat:
                    itemsOfGr = self.getItems(gr['Id'], False)
                    if itemsOfGr and len(itemsOfGr) > 0:
                        for it in itemsOfGr:
                            itSql = "DELETE FROM Item WHERE Id=" + str(it['Id'])
                            self.connection.execute(itSql)

                    grSql = "DELETE FROM ItemGroup WHERE Id=" + str(gr['Id'])
                    self.connection.execute(grSql)

            sql = "DELETE FROM ItemCategory WHERE Id = " + str(categoryId)
            self.connection.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

        self.disconnect()

    # ITEM GROUP BUSINESS
    def saveItemGroup(self, group):
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM ItemGroup WHERE Id = """ + str(group['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO ItemGroup(Id, ItemGroupCode, ItemGroupName, ItemCategoryId, GroupImage)
                        VALUES("""+ str(group['id']) +""", '""" + group['itemGroupCode'] + """',
                        '"""+ group['itemGroupName'] +"""', """+ str(group['itemCategoryId']) +""", '"""+ (group['groupImage'] if group['groupImage'] else '') +"""')""")
            else:
                self.connection.execute("""
                        UPDATE ItemGroup SET ItemGroupCode='"""+ group['itemGroupCode'] +"""',
                            ItemGroupName='"""+ group['itemGroupName'] +"""',
                            ItemCategoryId="""+ str(group['itemCategoryId']) +""", 
                            GroupImage='"""+ (group['groupImage'] if group['groupImage'] else '') +"""' WHERE Id="""+ str(group['id']) +"""
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
                    'GroupImage': r[3],
                    'ItemCategoryId': r[4]
                }
        except:
            pass
        self.disconnect()
        return returnData


    def getItemGroups(self, categoryId, disconnect=True):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM ItemGroup WHERE ItemCategoryId=" + str(categoryId)).fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemGroupCode': r[1],
                    'ItemGroupName': r[2],
                    'GroupImage': r[3],
                    'ItemCategoryId': r[4]
                })
        except:
            pass
        
        if disconnect:
            self.disconnect()
        return returnData


    def getProperItemGroups(self, categoryId, employeeId, disconnect=True):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM ItemGroup AS ig WHERE ItemCategoryId=" + str(categoryId) +
                " AND EXISTS(SELECT * FROM EmployeeCredit AS cr WHERE cr.EmployeeId = "+ str(employeeId) 
                +" AND ((cr.ItemCategoryId = ig.ItemCategoryId AND cr.ItemGroupId IS NULL) OR (cr.ItemGroupId = ig.Id))) "
                ).fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemGroupCode': r[1],
                    'ItemGroupName': r[2],
                    'GroupImage': r[3],
                    'ItemCategoryId': r[4]
                })
        except:
            pass
        
        if disconnect:
            self.disconnect()
        return returnData


    def deleteItemGroup(self, groupId):
        self.connect()
        try:
            itemsOfGroup = self.getItems(groupId, False)
            if itemsOfGroup and len(itemsOfGroup) > 0:
                for item in itemsOfGroup:
                    itemSql = "DELETE FROM Item WHERE Id=" + str(item['Id'])
                    self.connection.execute(itemSql)

            sql = "DELETE FROM ItemGroup WHERE Id = " + str(groupId)
            self.connection.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

        self.disconnect()

    # ITEM BUSINESS
    def saveItem(self, item):
        self.connect()
        try:
            existingRecord = self.connection.execute("""
                    SELECT * FROM Item WHERE Id = """ + str(item['id']) + """
                """).fetchone()
            
            if existingRecord is None:
                self.connection.execute("""
                        INSERT INTO Item(Id, ItemCode, ItemName, ItemCategoryId, ItemGroupId, ItemImage)
                        VALUES("""+ str(item['id']) +""", '""" + item['itemCode'] + """',
                        '"""+ item['itemName'] +"""', """+ str(item['itemCategoryId']) +""", """+ str(item['itemGroupId']) +""", '"""+ (item['itemImage'] if item['itemImage'] else '') +"""')""")
            else:
                self.connection.execute("""
                        UPDATE Item SET ItemCode='"""+ item['itemCode'] +"""',
                            ItemName='"""+ item['itemName'] +"""',
                            ItemCategoryId="""+ str(item['itemCategoryId']) +""", ItemGroupId="""+ str(item['itemGroupId']) +""", 
                            ItemImage='"""+ (item['itemImage'] if item['itemImage'] else '')
                            +"""' WHERE Id="""+ str(item['id']) +"""
                    """)

            self.connection.commit()
        except Exception as e:
            print(e)
            pass
        self.disconnect()

    
    def getItems(self, groupId, disconnect=True):
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
                    'ItemCategoryId': r[4],
                    'ItemImage': r[5],
                })
        except:
            pass
        
        if disconnect:
            self.disconnect()
        return returnData

    def getProperItems(self, groupId, categoryId, employeeId, disconnect=True):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Item AS it WHERE ItemGroupId=" + str(groupId) + " AND " +
                "EXISTS(SELECT * FROM EmployeeCredit AS cr WHERE cr.EmployeeId = "+ str(employeeId) +" AND cr.ActiveCredit > 0 AND ((cr.ItemCategoryId = "+ str(categoryId) +" AND cr.ItemGroupId IS NULL AND cr.ItemId IS NULL) OR (cr.ItemGroupId = it.ItemGroupId AND cr.ItemId IS NULL) OR (cr.ItemId = it.Id))) "
                + " AND EXISTS(SELECT * FROM Spiral AS sr WHERE sr.ItemId = it.Id AND sr.ActiveQuantity > 0)").fetchall()
            for r in rows:
                returnData.append({
                    'Id': r[0],
                    'ItemCode': r[1],
                    'ItemName': r[2],
                    'ItemGroupId': r[3],
                    'ItemCategoryId': r[4],
                    'ItemImage': r[5],
                })
        except:
            pass
        
        if disconnect:
            self.disconnect()
        return returnData

    def getItemsByCategory(self, categoryId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Item WHERE ItemCategoryId=" + str(categoryId)).fetchall()
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
                    'ItemCategoryId': r[4],
                    'ItemImage': r[5],
                }
        except:
            pass
        self.disconnect()
        return returnData

    def deleteItem(self, itemId):
        self.connect()
        try:
            sql = "DELETE FROM Item WHERE Id = " + str(itemId)
            self.connection.execute(sql)
            self.connection.commit()
        except Exception as e:
            print(e)

        self.disconnect()
    # SPIRAL BUSINESS
    def saveSpirals(self, spirals):
        self.connect()
        try:
            self.connection.execute("DELETE FROM Spiral")
            for item in spirals:
                self.connection.execute("""
                        INSERT INTO Spiral(Id, SpiralNo, ItemCategoryId, ItemId, ActiveQuantity)
                        VALUES("""+ str(item['id']) +""", '""" + str(item['posOrders']) + """',
                        """+ (str(item['itemCategoryId']) if item['itemCategoryId'] else 'NULL') +""", """
                        + (str(item['itemId']) if item['itemId'] else 'NULL') +""", """+ ( str(item['activeQuantity']) if item['activeQuantity'] else 'NULL' )+""")""")
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
                ir = self.connection.execute("SELECT ItemGroupId FROM Item WHERE Id = " + str(r[1])).fetchone()
                returnData = {
                    "ItemCategoryId": r[0],
                    "ItemId": r[1],
                    "ItemGroupId": int(ir[0]) if ir and ir[0] else None
                }
        except Exception as e:
            pass
        self.disconnect()
        return returnData

    def getProperSpirals(self, itemId):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Spiral WHERE ItemId = " + str(itemId) + " AND ActiveQuantity > 0").fetchall()
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

    def getAllSpirals(self):
        returnData = []
        self.connect()
        try:
            rows = self.connection.execute("SELECT * FROM Spiral ORDER BY SpiralNo").fetchall()
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
            self.connection.commit()
        except:
            pass
        self.disconnect()

        self.connect()
        try:
            self.connection.execute("DELETE FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId))
            for item in credits:
                self.connection.execute("""
                        INSERT INTO EmployeeCredit(Id, EmployeeId, ItemCategoryId, ItemGroupId, ItemId, 
                            ActiveCredit,RangeType,RangeLength,CreditByRange,RangeCredit, CreditEndDate)
                        VALUES("""+ str(item['id']) +""", """ + str(item['employeeId']) + """,
                        """+ str(item['itemCategoryId']) +""", """+ (str(item['itemGroupId']) if item['itemGroupId'] else 'NULL') +""", """+ (str(item['itemId']) if item['itemId'] else 'NULL') +""", """+ 
                            str(item['activeCredit']) +""", 
                        """+ (str(item['rangeType']) if item['rangeType'] else 'NULL') +""", 
                        """+ (str(item['rangeLength']) if item['rangeLength'] else 'NULL') +""",
                        """+ (str(item['creditByRange']) if item['creditByRange'] else 'NULL') +""",
                        """+ (str(item['rangeCredit']) if item['rangeCredit'] else 'NULL') + """,
                        '"""+ (str(item['creditEndDate'])[0:10] if item['creditEndDate'] else 'NULL') +"""'
                        )""")
            self.connection.commit()
        except Exception as e:
            pass
        self.disconnect()


    def getCreditInfo(self, employeeId, itemCategoryId, itemGroupId = None, itemId = None):
        returnData = {
            "ActiveCredit": 0,
            "RangeType": 4,
            "RangeLength": 1,
            "CreditByRange": 0,
        }

        self.connect()
        try:
            r = None
            if itemId:
                r = self.connection.execute("SELECT RangeCredit, RangeType, RangeLength, CreditByRange FROM EmployeeCredit WHERE CreditEndDate >= DATE() AND EmployeeId = " + str(employeeId) 
                    + " AND ItemId = " + str(itemId)).fetchone()
            elif not itemGroupId:
                r = self.connection.execute("SELECT RangeCredit, RangeType, RangeLength, CreditByRange FROM EmployeeCredit WHERE CreditEndDate >= DATE() AND EmployeeId = " + str(employeeId) 
                    + " AND ItemCategoryId = " + str(itemCategoryId)).fetchone()
            else:
                r = self.connection.execute("SELECT RangeCredit, RangeType, RangeLength, CreditByRange FROM EmployeeCredit WHERE CreditEndDate >= DATE() AND EmployeeId = " + str(employeeId) 
                    + " AND ItemCategoryId = " + str(itemCategoryId) + " AND (ItemGroupId IS NULL OR ItemGroupId = "+ str(itemGroupId) +")").fetchone()
            if r:
                returnData['ActiveCredit'] = int(r[0])
                returnData['RangeType'] = (int(r[1]) if r[1] else 4)
                returnData['RangeLength'] = (int(r[2]) if r[2] else 1)
                returnData['CreditByRange'] = (int(r[3]) if r[3] else 0)
        except Exception as e:
            pass
        self.disconnect()

        return returnData

    
    def checkEmployeeHasCredit(self, employeeId, itemCategoryId, itemGroupId = None) -> bool:
        hasCredit = False
        self.connect()
        try:
            if not itemGroupId:
                r = self.connection.execute("SELECT RangeCredit FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId) 
                    + " AND ItemCategoryId = " + str(itemCategoryId) + " AND CreditEndDate >= DATE()").fetchone()
            else:
                r = self.connection.execute("SELECT RangeCredit FROM EmployeeCredit WHERE EmployeeId = " + str(employeeId) 
                    + " AND ItemCategoryId = " + str(itemCategoryId) + " AND CreditEndDate >= DATE() AND(ItemGroupId IS NULL OR ItemGroupId = "+ str(itemGroupId) +")").fetchone()
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
            self.connection.execute("UPDATE EmployeeCredit SET RangeCredit = RangeCredit - 1 WHERE EmployeeId = " + str(employeeId) 
                + " AND ItemCategoryId = " + str(itemCategoryId) + " AND CreditEndDate >= DATE()")
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