import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

passwords_to_try = ['postgres', 'admin', 'root', '1234', '12345', 'password', '']
success = False

for pwd in passwords_to_try:
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password=pwd)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE clink;")
        cur.close()
        conn.close()
        print(f"SUCCESS with password: '{pwd}'")
        success = True
        break
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database already exists! Password is '{pwd}'")
        success = True
        break
    except Exception as e:
        pass

if not success:
    print("FAILED")
    sys.exit(1)
