import sqlite3

def checkTableText():
    conn = sqlite3.connect("db_ann.db")
    c = conn.cursor()
                
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='string' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : 
        print('Table text exists.')
    else :
        conn.execute("CREATE TABLE string (text varchar (255), clean_text varchar (255));")
        print('Table text created')
                
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()

def checkTableFile():
    conn = sqlite3.connect("db_ann.db")
    c = conn.cursor()
                
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='file' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : 
        print('Table file exists.')
    else :
        conn.execute("CREATE TABLE file (text varchar (255), clean_text varchar (255));")
        print('Table file created')
                
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()

checkTableText()
checkTableFile()

def input_text(a, b):
    conn = sqlite3.connect("db_ann.db")
    conn.execute("insert into string (text, clean_text) values (?, ?)",(a, b))
    conn.commit()
    conn.close()
    print("Data berhasil disimpan di db sqlite")

def input_file(a):
    a.rename(columns={'Tweet': 'text', 'space': 'clean_text'}, inplace=True)
    conn = sqlite3.connect('db_ann.db') 
    a.to_sql('file', con=conn, index=False, if_exists='append') ## if_exists => replace => bikin tabel baru, menghapus yg lama
    conn.close()
    print("Data berhasil disimpan di db sqlite")
