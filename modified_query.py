import sqlite3

class DB():
    def __init__(self, name: str):
        self.__session = sqlite3.connect(name)
        self.__cursor = self.__session.cursor()
    
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

db = DB('database.db')

print(db.getProfileInfo(user_id=1))
print(db.getCartInfo(user_id=1))
print(db.getPurchasedOrders(user_id=1))

del db