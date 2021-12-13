import sqlite3

class DB():
    def __init__(self):
        self.__session = sqlite3.connect('database.db')
        self.__cursor = self.__session.cursor()
    
    def createTemporaryDB(self):
        self.__tempsession = sqlite3.connect("file::memory:?cache=shared")
        self.__tempcursor = connection.cursor()
        self.__tempcursor.executescript(
            """
            CREATE TABLE "user" (
                "id"	INTEGER,
                "email"	TEXT,
                "username"	TEXT,
                "password"	TEXT,
                "phone_number"	TEXT,
                "address"	TEXT,
                "age"	INTEGER,
                "birth_date"	TEXT,
                "created_at"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            )

            CREATE TABLE "product_category" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT,
                "description"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            )

            CREATE TABLE "product" (
                "id"	INTEGER NOT NULL,
                "name"	TEXT,
                "description"	TEXT,
                "category_id"	INTEGER,
                "price"	INTEGER,
                "amount"	INTEGER,
                "discount_rate"	INTEGER,
                FOREIGN KEY("category_id") REFERENCES "product_category"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            )

            CREATE TABLE "cart_item" (
                "id"	INTEGER NOT NULL,
                "user_id"	INTEGER,
                "product_id"	INTEGER,
                "price"	INTEGER,
                "amount"	INTEGER,
                "order_id"	INTEGER,
                "date_created"	TEXT,
                FOREIGN KEY("user_id") REFERENCES "user"("id"),
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("product_id") REFERENCES "product"("id")
            )

            CREATE TABLE "purchased_order" (
                "id"	INTEGER NOT NULL,
                "user_id"	INTEGER,
                "total_price"	INTEGER,
                "user_email"	TEXT,
                "user_phone"	TEXT,
                "user_note"	TEXT,
                "address"	TEXT,
                "created_at"	TEXT,
                FOREIGN KEY("user_id") REFERENCES "user"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            )
            """
        )
    
    def getProfileInfo(self, user_id: int):
        request = "SELECT email, username, password, phone_number, address, birth_date, created_at FROM user WHERE user.id = :user_id;"
        return self.__cursor.execute(request, {'user_id': user_id}).fetchall()
    
    def getCartInfo(self, user_id: int):
        request = "SELECT (SELECT name FROM product WHERE id = product_id) AS product_name, price, amount, date_created FROM cart_item WHERE cart_item.user_id = :user_id AND cart_item.order_id IS NULL;"
        return self.__cursor.execute(request, {'user_id': user_id}).fetchall()

    def getPurchasedOrders(self, user_id: int):
        request = "SELECT total_price, user_email, user_phone, user_note, address, created_at AS payment_received_at FROM purchased_order WHERE purchased_order.user_id = :user_id;"
        return self.__cursor.execute(request, {'user_id': user_id}).fetchall()
        
    def __del__(self):
        self.__session.close()

db = DB()

print(db.getProfileInfo(user_id=1))
print(db.getCartInfo(user_id=1))
print(db.getPurchasedOrders(user_id=1))

del db