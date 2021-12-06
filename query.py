import sqlite3

user_id = 1

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute(
    '''
    SELECT 
	    email AS email, 
	    username AS username, 
	    password AS password, 
	    phone_number AS phone_number, 
	    address AS address, 
	    birth_date AS birth_date, 
	    created_at AS created_at 
    FROM user 
    WHERE user.id = :user_id;
    ''', {'user_id': user_id}
)

print(cursor.fetchall())

cursor.execute(
    '''
     SELECT
	    (SELECT name FROM product WHERE id = product_id) AS product_name,
	    price AS price,
	    amount AS amount, 
	    date_created AS date_when_added
    FROM cart_item
    WHERE cart_item.user_id = :user_id AND cart_item.order_id IS NULL;
    ''', {'user_id': user_id}
)

print(cursor.fetchall())

cursor.execute(
    '''
    SELECT
        total_price AS total_price,
        user_email AS user_email,
        user_phone AS user_phone,
        user_note AS user_note,
        address AS address,
        created_at AS payment_received_at
    FROM purchased_order
    WHERE purchased_order.user_id = :user_id;
    ''', {'user_id': user_id}
)

print(cursor.fetchall())

connection.close()