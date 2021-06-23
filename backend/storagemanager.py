#!/usr/bin/python3

from datetime import datetime
import mysql.connector as sql

from datatypes import CategoryBase, ItemBase, ServerResults

class StorageManager():
    def __init__(self):
        pass

    @staticmethod
    def __connectDb():
        mydb = sql.connect(
            host="localhost",
            user="storagemanager",
            password="storagemanager",
            database="storagemanager"
        )
        mycursor = mydb.cursor()
        return (mydb, mycursor)

    def addCategory(self, categoryRaw: dict()) -> ServerResults:
        category = CategoryBase(**categoryRaw)
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        query = "insert into category (categoryName, description) values (%s, %s)"
        values = (category.name, category.description)
        try:
            cursor.execute(query, values)
            database.commit()
            database.close()
        except sql.errors.IntegrityError as e:
            if '1062' in str(e):
                return ServerResults.DB_DUPLICATE_ENTRY
            else:
                return ServerResults.RESULTS_UNKNOWN
        return ServerResults.OK

    def retrieveCategory(self) -> CategoryBase:
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        query = "select * from category"
        values = ()
        try:
            cursor.execute(query, values)
            dbResults = cursor.fetchall()
            results = list()
            database.close()
            for dbResult in dbResults:
                results.append({"name":dbResult[0], "description":dbResult[1]})
            result = results
            return result
        except Exception as e:
            print(str(e))

    @staticmethod
    def getExistingAmount(uuid: str) -> int:
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        query = "select amount from items where uuid = %s"
        values = (uuid,)
        cursor.execute(query, values)
        dbResults = cursor.fetchone()
        database.close()
        if dbResults is None:
            return 0
        else:
            return int(dbResults[0])

    @staticmethod
    def getEarliestExpireDate(uuid: str, currentExpireDate: str) -> str:
        current = datetime.strptime(currentExpireDate, "%Y-%m-%d").date()
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        query = "select expire from items where uuid = %s"
        values = (uuid,)
        cursor.execute(query, values)
        dbResults = cursor.fetchone()
        database.close()
        if dbResults is None:
            return currentExpireDate
        else:
            existing = dbResults[0]
            if current > existing:
                return str(existing)
            else:
                return str(current)


    def addItem(self, itemRaw: dict()) -> ServerResults:
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        existingAmount = StorageManager.getExistingAmount(itemRaw['uuid'])
        earliestExpire = StorageManager.getEarliestExpireDate(itemRaw['uuid'], itemRaw['expireDate'])
        try:
            query = "insert into items (uuid, itemName, amount, expire, modifiedDate) values (%s, %s, %s, %s, %s) \
                on duplicate key update amount=%s, expire=%s, modifiedDate=%s"
            values = (itemRaw['uuid'], itemRaw['name'], existingAmount + itemRaw['amount'],
                    earliestExpire, str(datetime.today().date()),
                    existingAmount + itemRaw['amount'],
                    earliestExpire,
                    str(datetime.today().date()))
            cursor.execute(query, values)
            database.commit()
            database.close()
        except Exception as e:
            print(e)

        return ServerResults.OK