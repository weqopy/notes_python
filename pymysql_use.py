import pymysql
import os

db_username = os.environ.get('mysql_username')
db_password = os.environ.get('mysql_password')
db = pymysql.connect('localhost', 'db_username', 'db_password', 'test')

cursor = db.cursor()

cursor.execute('drop table if exists employee')

# 创建表
sql_create_1 = """create table employee (
                  first_name char(20) not null,
                  age tinyint,
                  sex char(1),
                  income float
)"""

cursor.execute(sql_create_1)

# 创建表中新内容
sql_insert_1 = """insert into employee(
                  first_name, age, sex, income)
                  values('mac', 20, 'M', 2000)"""
sql_insert_2 = """insert into employee(
                  first_name, age, sex, income)
                  values('tom', '22', 'F', 2330)"""
try:
    cursor.execute(sql_insert_1)
    cursor.execute(sql_insert_2)
    db.commit()
except:
    db.rollback()

sql_select_1 = 'select * from employee where income > "{}"'.format(1000)

try:
    cursor.execute(sql_select_1)
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        age = row[1]
        sex = row[2]
        income = row[3]
        print("fname={}, age={}, sex={}, income={}".format(fname, age, sex,
                                                           income))
except:
    print('Error: unable to fetch data')

db.close()
