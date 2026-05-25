import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="182022",
        database="techrepair",
        auth_plugin="mysql_native_password"
    )
    print("Conexao OK!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes LIMIT 5")
    print("Clientes:", cursor.fetchall())
    conn.close()
except Exception as e:
    print(f"ERRO: {e}")

# Tentativa 2 - sem auth_plugin
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="182022",
        database="techrepair"
    )
    print("Conexao OK (sem auth_plugin)!")
    conn.close()
except Exception as e:
    print(f"ERRO sem auth_plugin: {e}")
