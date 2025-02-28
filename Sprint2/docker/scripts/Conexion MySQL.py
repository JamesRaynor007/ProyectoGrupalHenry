import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Conexión a MySQL exitosa")
    except Error as e:
        print(f"Error '{e}' ocurrió")

    return connection

if __name__ == "__main__":
    connection = create_connection("127.0.0.1", "root", "root", "testdb")
