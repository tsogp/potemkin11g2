import sqlite3

class DB():
    def __init__(self):
        self.__session = sqlite3.connect('database.db')
        self.__cursor = self.__session.cursor()
    
    def createTemporaryDB(self, db_name: str):
        self.__tempsession = sqlite3.connect(db_name)
        self.__tempcursor = self.__tempsession.cursor()
        
        self.__tempcursor.executescript(
            """
            BEGIN TRANSACTION;
            CREATE TABLE IF NOT EXISTS "product_category" (
                    "id"    INTEGER NOT NULL,
                    "name"  TEXT,
                    "description"   TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
            );
            INSERT INTO product_category VALUES(1,'Fried','Fried coffee beans');
            INSERT INTO product_category VALUES(2,'Raw','Raw coffee beans');
            INSERT INTO product_category VALUES(3,'Fermented','Fermented coffee beans');
            CREATE TABLE IF NOT EXISTS "user" (
                    "id"    INTEGER,
                    "email" TEXT,
                    "username"      TEXT,
                    "password"      TEXT,
                    "phone_number"  TEXT,
                    "address"       TEXT,
                    "age"   INTEGER,
                    "birth_date"    TEXT,
                    "created_at"    TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
            );
            INSERT INTO user VALUES(1,'1@a.ru','bob','123','719-327-1876','Landline-Colorado-USA',19,'2002-07-31','2021-11-22');
            INSERT INTO user VALUES(2,'2@a.ru','jacob','123','570-609-2534','Wyoming-PA-USA',48,'1973-08-04','2021-11-22');
            INSERT INTO user VALUES(3,'3@a.ru','jared','123','706-321-1318','Columbus-Georgia-USA',26,'1995-03-12','2021-11-23');
            INSERT INTO user VALUES(4,'4@a.ru','anthony','123','748-637-1982','Columbus-Georgia-USA',60,'1961-10-01','2021-05-01');
            CREATE TABLE IF NOT EXISTS "product" (
                    "id"    INTEGER NOT NULL,
                    "name"  TEXT,
                    "description"   TEXT,
                    "category_id"   INTEGER,
                    "price" INTEGER,
                    "amount"        INTEGER,
                    "discount_rate" INTEGER,
                    FOREIGN KEY("category_id") REFERENCES "product_category"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
            );
            INSERT INTO product VALUES(1,'Arabica','Arabica coffee beans',1,2500,10,0);
            INSERT INTO product VALUES(2,'Liberica','Liberica coffee beans',1,3000,10,0);
            INSERT INTO product VALUES(3,'Robusta','Robusta coffee beans',2,4000,10,0);
            CREATE TABLE IF NOT EXISTS "cart_item" (
                    "id"    INTEGER NOT NULL,
                    "user_id"       INTEGER,
                    "product_id"    INTEGER,
                    "price" INTEGER,
                    "amount"        INTEGER,
                    "order_id"      INTEGER,
                    "date_created"  TEXT,
                    FOREIGN KEY("user_id") REFERENCES "user"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("product_id") REFERENCES "product"("id")
            );
            INSERT INTO cart_item VALUES(1,1,1,2500,3,1,'2021-11-23');
            INSERT INTO cart_item VALUES(2,2,2,3000,5,2,'2021-11-21');
            INSERT INTO cart_item VALUES(3,3,3,4000,2,3,'2021-11-22');
            INSERT INTO cart_item VALUES(4,1,3,4000,4,NULL,'2021-12-05');
            CREATE TABLE IF NOT EXISTS "purchased_order" (
                    "id"    INTEGER NOT NULL,
                    "user_id"       INTEGER,
                    "total_price"   INTEGER,
                    "user_email"    TEXT,
                    "user_phone"    TEXT,
                    "user_note"     TEXT,
                    "address"       TEXT,
                    "created_at"    TEXT,
                    FOREIGN KEY("user_id") REFERENCES "user"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
            );
            INSERT INTO purchased_order VALUES(1,1,7500,'1@a.ru','719-327-1876','please deliver soon!','Landline-Colorado-USA','2021-11-22');
            INSERT INTO purchased_order VALUES(2,2,15000,'2@a.ru','570-609-2534','please deliver soon!','Wyoming-PA-USA','2021-11-22');
            INSERT INTO purchased_order VALUES(3,3,12000,'3@a.ru','706-321-1318','please deliver soon!','Columbus-Georgia-USA','2021-11-23');
            DELETE FROM sqlite_sequence;
            INSERT INTO sqlite_sequence VALUES('product_category',3);
            INSERT INTO sqlite_sequence VALUES('user',4);
            INSERT INTO sqlite_sequence VALUES('product',3);
            INSERT INTO sqlite_sequence VALUES('cart_item',4);
            INSERT INTO sqlite_sequence VALUES('purchased_order',3);
            COMMIT;
            """
        )

        self.__tempsession.close()
    
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

db.createTemporaryDB(db_name='temp.db')

del db