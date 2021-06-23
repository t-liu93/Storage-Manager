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

    def addItem(self, itemRaw: dict()) -> ServerResults:
        item = ItemBase(**itemRaw)
        dbConnection = StorageManager.__connectDb()
        database = dbConnection[0]
        cursor = dbConnection[1]
        try:
            query = "insert into items (uuid, itemName, amount, modifiedDate) values (%s, %s, %s, %s) \
                on duplicate key update amount=amount+%s, modifiedDate=%s"
            values = (item.uuid, item.name, item.amount,
                    str(datetime.today().date()),
                    item.amount,
                    str(datetime.today().date()))
            cursor.execute(query, values)
            query = "insert into itemsexpire (uuid, expire, amount) values (%s, %s, %s) \
                on duplicate key update amount=amount+%s"
            values = (item.uuid, item.expireDate[0].date, item.expireDate[0].amount, item.expireDate[0].amount)
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
        query = "select items.*, itemscategory.category, itemsexpire.expire, itemsexpire.amount from items \
            inner join itemscategory on items.uuid = itemscategory.uuid \
            inner join itemsexpire on items.uuid = itemsexpire.uuid \
            where items.uuid = %s"
        values = (uuid,)
        cursor.execute(query, values)
        itemResults = cursor.fetchall()
        if len(itemResults) == 0:
            return None
        categories = []
        expireDates = []
        for item in itemResults:
            if item[4] not in categories:
                categories.append(item[4])
        for item in itemResults:
            expireDate = {'date':str(item[5]), 'amount': item[6]}
            expireDates.append(expireDate)
        database.close()
        itemResult = itemResults[0]
        resultRaw = {
            'uuid': itemResult[0],
            'name': itemResult[1],
            'amount': itemResult[2],
            'category': categories,
            'expireDate': expireDates,
            'lastModifiedDate': str(itemResult[4])
        }
        result = ItemBase(**resultRaw)
        return result