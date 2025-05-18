import psycopg2

email = 'majid@gmail.com'



conn = psycopg2.connect(dbname="task_manager_db",
        user="majid",
        password="1361MAJIDhashemi",  # Update with real password
        host="localhost")
cur = conn.cursor()

cur.execute("SELECT password, role FROM users WHERE email = %s", (email,))

result = cur.fetchone()

print(result)  # Example output: ('hashedpassword123', 'admin')

cur.close()
conn.close()
