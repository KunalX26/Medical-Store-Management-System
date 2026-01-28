import pymysql

def create_connection():
    cn=pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='vgt',
        autocommit=True
    )
    cur=cn.cursor()
    return cur

def admindata(email):
    cur=create_connection()
    sql="select * from admindata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    data=None
    if (n==1):
        data=cur.fetchone()
    return data

def medicaldata(email):
    cur=create_connection()
    sql="select * from medicaldata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    data=None
    if (n==1):
        data=cur.fetchone()
    return data

def check_photo(email):
    cur =  create_connection()
    cur.execute("SELECT * FROM photodata where email='" + email + "'")
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo




