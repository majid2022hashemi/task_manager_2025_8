import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="task_manager_db",
        user="majid",
        password="1361MAJIDhashemi",  # Update with real password
        host="localhost"
    )
