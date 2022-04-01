import sqlite3

class DataMigrator():
    def __init__(self):
        self.prepareMigrationScript()


    def migrate(self, connection):
        if connection:
            for scr in self.script:
                try:
                    connection.execute(scr)
                except:
                    pass
            connection.commit()


    def prepareMigrationScript(self):
        self.script = ["""
            CREATE TABLE IF NOT EXISTS MachineConfig(
                Id INT PRIMARY KEY, 
                Code NVARCHAR(100), 
                Name NVARCHAR(100),
                ApiAddr NVARCHAR(300),
                ModbusType NVARCHAR(10),
                ModbusServerAddr NVARCHAR(100),
                ModbusServerPort NVARCHAR(100),
                ModbusCoilPushItem NVARCHAR(50),
                ModbusCoilServiceFlag NVARCHAR(50),
                ModbusRegisterSpiralNo NVARCHAR(50),
                Rows INT,
                Cols INT)    
            """,
            """
                CREATE TABLE IF NOT EXISTS Employee(
                    Id INT PRIMARY KEY,
                    EmployeeCode NVARCHAR(200),
                    EmployeeName NVARCHAR(200),
                    CardNo NVARCHAR(200),
                    CardHexNo NVARCHAR(200),
                    DepartmentName NVARCHAR(200)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS ItemCategory(
                    Id INT PRIMARY KEY,
                    ItemCategoryCode NVARCHAR(200),
                    ItemCategoryName NVARCHAR(200),
                    CategoryImage TEXT,
                    CreditRangeType INT,
                    CreditByRange INT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS ItemGroup(
                    Id INT PRIMARY KEY,
                    ItemGroupCode NVARCHAR(200),
                    ItemGroupName NVARCHAR(200),
                    GroupImage TEXT,
                    ItemCategoryId INT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS Item(
                    Id INT PRIMARY KEY,
                    ItemCode NVARCHAR(200),
                    ItemName NVARCHAR(200),
                    ItemGroupId INT,
                    ItemCategoryId INT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS Spiral(
                    Id INT PRIMARY KEY,
                    SpiralNo INT,
                    ItemCategoryId INT,
                    ItemId INT,
                    ActiveQuantity INT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS EmployeeCredit(
                    Id INT PRIMARY KEY,
                    EmployeeId INT,
                    ItemCategoryId INT,
                    ItemGroupId INT NULL,
                    ItemId INT NULL,
                    ActiveCredit INT,
                    RangeType INT,
                    RangeLength INT,
                    CreditByRange INT,
                    RangeCredit INT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS CreditConsuming(
                    Id INT PRIMARY KEY,
                    EmployeeId INT,
                    ItemCategoryId INT,
                    Credit INT,
                    SyncStatus INT
                )
            """]
