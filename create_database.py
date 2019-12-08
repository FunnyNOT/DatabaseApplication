import sqlite3

#Create SQlite database function on disk memory
def create_Database():
    conn  = sqlite3.connect("sqlite/application_database.db")
    c= conn.cursor()
    c.execute("""CREATE TABLE users_info (
                 ID integer  PRIMARY KEY AUTOINCREMENT,
                 Username text,
                 Password text,
                 Email    text,
                 Phone_Number integer,
                 First_Name text,
                 Last_Name text,
                 Access_Level integer DEFAULT 0,
                 ID_Xwrwn_Prosvasis text DEFAULT null
                 )""")
    c.execute("""CREATE TABLE xwroi_idrymatos(
                 ID_xwrou integer  PRIMARY KEY AUTOINCREMENT,
                 xrisi_xwrou text,
                 onoma_xwrou text,
                 ID_epoptwn text DEFAULT null 
                 )""")
    c.execute("""CREATE TABLE yliko_xwrwn(
                 ID_ylikou integer  PRIMARY KEY AUTOINCREMENT,
                 ID_Xwrou text,
                 perigrafi_xrisis text ,
                 typos text,
                 posotita text,
                 katastasi text ,
                 etairia text  ,
                 montelo text ,
                 onomasia_organou text  DEFAULT null,
                 xronos_ktisis text,
                 seiriakos_arithmos text,
                 skopos_xrisis text  DEFAULT null,
                 varos text DEFAULT null,
                 diathesimotita text  DEFAULT null,
                 dinatotita_metakinisis text  DEFAULT null,
                 katastasi_daneismou text DEFAULT 'Available',
                 katigoria text DEFAULT null,
                 ypokatigoria text DEFAULT null,
                 lekseis_kleidia text
                 )""")
    c.execute("""CREATE TABLE daneismos(
                 ID_ylikou integer  PRIMARY KEY,
                 onoma_xristi text,
                 epitheto_xristi text
                 )""")
    insert_Admin(conn, c)
    insert_Supervisor(conn, c)
    insert_User(conn, c)
    return conn


# Insert Admin Key to Database function
def insert_Admin(connection, cursor):
    with connection:
        cursor.execute("""INSERT INTO users_info('Username','Password','Email','Phone_Number','First_Name','Last_Name','Access_Level')
                         VALUES ('admin','admin1234','admin@gmail.com',2510462147,'Onoma','Epitheto',2)
                         """)


# Insert User Key to Database function
def insert_User(connection, cursor):
    with connection:
        cursor.execute("""INSERT INTO users_info('Username','Password','Email','Phone_Number','First_Name','Last_Name','Access_Level')
                         VALUES ('user','user1234','user@gmail.com',2510462147,'User','User',0)
                         """)


# Insert Supervisor Key to Database function
def insert_Supervisor(connection, cursor):
    with connection:
        cursor.execute("""INSERT INTO users_info('Username','Password','Email','Phone_Number','First_Name','Last_Name','Access_Level')
                         VALUES ('supervisor','super1234','super@gmail.com',2510462147,'Superv','Superv',1)
                         """)


