import os
import datetime

database = 'qardio'
password = ''
now = str(datetime.datetime.now()).replace(' ', '').replace(':', '').replace('.', '')

os.system(f'sudo /usr/local/mysql/bin/mysqldump -u root -p{password} {database} > backups/{database}_db_{now}.sql')