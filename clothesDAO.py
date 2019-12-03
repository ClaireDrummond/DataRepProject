import mysql.connector
class ClothesDAO:
    db=""
    def __init__(self): 
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        #user="datarep",  # this is the user name on my mac
        #passwd="password" # for my mac
        database="datarepresentation"
        )
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into clothes (item, designer, price) values (%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from clothes"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return resultArray

    def findByBarcode(self, barcode):
        cursor = self.db.cursor()
        sql="select * clothes where barcode = %s"
        values = (barcode,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def update(self, values):
        cursor = self.db.cursor()
        sql="update clothes set items= %s, designer=%s, price=%s  where barcode = %s"
        cursor.execute(sql, values)
        self.db.commit()

    def delete(self, barcode):
        cursor = self.db.cursor()
        sql="delete from clothes where barcode = %s"
        values = (barcode,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['barcode','Item','Designer', "Price"]
        
        item = {}

        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        return(item)

clothesDAO = ClothesDAO()

