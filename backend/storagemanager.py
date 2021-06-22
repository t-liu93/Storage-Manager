#!/usr/bin/python3

import mysql.connector as sql

from datatypes import CategoryBase, ServerResults

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

    def addCategory(self, categoryRaw: dict()):
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