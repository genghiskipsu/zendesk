# https://stackoverflow.com/questions/69997623/query-mysql-database-with-python-using-sshtunnel-with-ssh-ppk-key-file

import pymysql
import json
from sshtunnel import SSHTunnelForwarder

creds = json.load(open('creds.json.bak', 'r'))

server = SSHTunnelForwarder(
    (creds['ssh_host'], 22),
    ssh_host_key=None,
    ssh_username=creds['ssh_user'],
    ssh_password=None,
    ssh_private_key=creds['ssh_keyLocation'],
    ssh_private_key_password=None,
    remote_bind_address=(creds['host'], 3306),
    local_bind_address=("localhost", 10022)
)

def run_query():
    cnx = pymysql.connect(
    user=creds['db_user'], 
    password=creds['db_password'],
    host="localhost",
    port=10022,
    database=creds['database'],
    cursorclass=pymysql.cursors.DictCursor
    ) 
	
    query = [
        "SET @startDate = '2023-05-22';",
        "SET @endDate = '2023-10-11';"
    ]
    
    results = []
    
    with cnx:
        with cnx.cursor() as cursor:
            for i in query:
                cursor.execute(cursor.mogrify(i))
                results.append(cursor.fetchall())
    print(results)

def main():
    server.start()
    run_query()
    server.stop()

if __name__ == '__main__':
    main()