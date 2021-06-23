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
        item = ItemBase(**itemRaw)
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        existingAmount = StorageManager.getExistingAmount(item.uuid)
        earliestExpire = StorageManager.getEarliestExpireDate(item.uuid, item.expireDate)
        try:
            query = "insert into items (uuid, itemName, amount, expire, modifiedDate) values (%s, %s, %s, %s, %s) \
                on duplicate key update amount=%s, expire=%s, modifiedDate=%s"
            values = (item.uuid, item.name, existingAmount + item.amount,
                    earliestExpire, str(datetime.today().date()),
                    existingAmount + item.amount,
                    earliestExpire,
                    str(datetime.today().date()))
            cursor.execute(query, values)
            for category in item.category:
                query = "insert into itemscategory (uuid, category) values (%s, %s) \
                    on duplicate key update uuid=%s"
                values = (item.uuid, category, item.uuid)
                cursor.execute(query, values)
            database.commit()
            database.close()
        except Exception as e:
            print(e)
            return ServerResults.RESULTS_UNKNOWN

        return ServerResults.OK

    def retrieveItem(self, uuid: str) -> ItemBase:
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        query = "select items.*, itemscategory.category from items \
            inner join itemscategory on items.uuid = itemscategory.uuid \
            where items.uuid = %s"
        values = (uuid,)
        cursor.execute(query, values)
        itemResults = cursor.fetchall()
        if len(itemResults) == 0:
            return None
        categories = []
        for item in itemResults:
            categories.append(item[5])
        database.close()
        itemResult = itemResults[0]
        resultRaw = {
            'uuid': itemResult[0],
            'name': itemResult[1],
            'amount': itemResult[2],
            'category': categories,
            'expireDate': str(itemResult[3]),
            'lastModifiedDate': str(itemResult[4])
        }
        result = ItemBase(**resultRaw)
        return result