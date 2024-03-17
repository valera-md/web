import psycopg2

def connect():
 conn = psycopg2.connect("dbname=chat_db user=postgres password=qazwsx host=localhost port=5889")
 curs = conn.cursor()
 return conn, curs
