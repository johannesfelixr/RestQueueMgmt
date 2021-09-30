import socket
import os
from _thread import *
from datetime import datetime
import sys
import json
import mysql.connector
import ssl
import traceback

#server preparation
ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.100.8'
port = 3456
serverkey='server.key'
serverpem='server.pem'
clientpem='client.pem'
ssl_version=None

#Constant untu mySQL
hostSQL="192.168.100.6",

#Fungsi Pendukung
#SSL
def ssl_wrap_socket(sock, ssl_version=None, keyfile=None, certfile=None, ciphers=None):

    #1. init a context with given version(if any)
    if ssl_version is not None and ssl_version in version_dict:
        #create a new SSL context with specified TLS version
        sslContext = ssl.SSLContext(version_dict[ssl_version])
        if option_test_switch == 1:
            print ("ssl_version loaded!! =", ssl_version)
    else:
        #if not specified, default
        sslContext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
    if ciphers is not None:
        #if specified, set certain ciphersuite
        sslContext.set_ciphers(ciphers)
        if option_test_switch == 1:
            print ("ciphers loaded!! =", ciphers)
    
    #server-side must load certfile and keyfile, so no if-else
    sslContext.load_cert_chain(certfile, keyfile)
    print ("ssl loaded!! certfile=", certfile, "keyfile=", keyfile)
    
    try:
        return sslContext.wrap_socket(sock, server_side = True)
    except ssl.SSLError as e:
        print ("wrap socket failed!")
        print (traceback.format_exc())

#Mencari maximum order number di mysql
def fetch_max_order_no():
    if db_connection.is_connected() == False:
        db_connection.connect()
    #db_cursor.execute("use restaurant")  # Interact with restaurant databse
    orderno  = 0
    query1 = "SELECT orderno FROM ordertable order by orderno DESC LIMIT 1"
    # implement query Sentence
    db_cursor.execute(query1) 
    print("No of Record Fetched:" + str(db_cursor.rowcount))
    if db_cursor.rowcount == 0:
        orderno = 1
    else:
        rows = db_cursor.fetchall()
        for row in rows:
            orderno = row[0]
        orderno = orderno + 1
    print("Max Order Id: " + str(orderno))
    return orderno


#definiskan fungsi callbacknya
#Kompilasi callback
def registerCb(jsonData): #untuk menerima request dari state register
    if db_connection.is_connected() == False:
        db_connection.connect()
    username=jsonData['username']
    password=jsonData['password']
    saldo='0'
    #verifikasi apakah username sudah terdaftar di mysql
    sqlQuery="SELECT * from usertable where username='%s'" %(username)
    db_cursor.execute(sqlQuery)
    data=db_cursor.fetchall()
    if (data!=[]):
        skirim={
            'response':'register',
            'status':'gagal',
            'keterangan' : "username sudah terdaftar sebelumnya"
        }
        return skirim
    try:
        #daftarkan
        sqlQuery="INSERT INTO usertable (username, password, saldo) VALUES (%s, %s, %s)"
        db_cursor.execute(sqlQuery, (username, password, saldo))
        db_connection.commit()
    except:
        skirim={
            'response':'register',
            'status':'gagal'
        }
    else:
        skirim={
            'response':'register',
            'status':'berhasil'
        }
        print("username "+username+" berhasil didaftarkan dengan saldo "+str(saldo))
    return skirim

def loginCb(jsonData): #memproses request dari state login
    #ambil data password
    if db_connection.is_connected() == False:
        db_connection.connect()
    username=jsonData["username"]
    password=jsonData["password"]
    try:
        #ambil password
        sqlQuery="SELECT password from usertable where username='%s'" %(
            username)
        db_cursor.execute(sqlQuery)
        passwordRef=db_cursor.fetchone()[0]
        #ambil saldo
        sqlQuery="SELECT saldo from usertable where username='%s'" %(
            username)
        db_cursor.execute(sqlQuery)
        saldo=db_cursor.fetchone()[0]
    except:
        skirim={
            'response': 'login',
            'status' : 'gagal',
            'keterangan' : 'umum'
        }
        print("login gagal umum")
    else :
        if (passwordRef==password):
            skirim={
                'response': 'login',
                'status' : 'berhasil',
                'saldo' : saldo
            }
        else :
            skirim={
                'response': 'login',
                'status' : 'gagal',
                'keterangan': 'password salah'
            }
            print("Password salah")
    return skirim
    
def pesanCb(jsonData): #memproses request dari state order/pesan
    if db_connection.is_connected() == False:
        db_connection.connect()
    orderno=int(fetch_max_order_no())
    paket=jsonData['paket']
    quantity=jsonData['quantity']
    status='paid'
    doo=str(datetime.now().strftime("%Y-%m-%d"))
    username=jsonData['username']
    password=jsonData['password']
    notes=jsonData['notes']
    totalHarga=jsonData['totalHarga']
    #Verifikasi password
    try:
        sqlQuery="SELECT password from usertable where username='%s'" %(
            username)
        db_cursor.execute(sqlQuery)
        passwordRef=db_cursor.fetchone()[0]
    except:
        skirim={
            'response': 'pesan',
            'status' : 'gagal',
            'keterangan' : 'verifikasi password gagal'
        }
        print("verifikasi pesan gagal umum")
        return skirim
    else :
        if (passwordRef!=password):
            skirim={
                'response': 'pesan',
                'status' : 'gagal',
                'keterangan': 'password salah'
            }
            return skirim
            print("Password salah")
    #ambil saldo saat ini
    sqlQuery="SELECT saldo from usertable where username='%s'" %(
        username)
    db_cursor.execute(sqlQuery)
    saldo=int(db_cursor.fetchone()[0])
    if (saldo>=int(totalHarga)):
        saldo=saldo-int(totalHarga)
    else:
        skirim={
            'response': 'pesan',
            'status': 'gagal',
            'keterangan' : 'saldo tidak cukup'
        }
        return skirim
    #update saldo
    sqlQuery="Update usertable set saldo='%s' where username='%s'" %(
        saldo, username)
    db_cursor.execute(sqlQuery)
    db_connection.commit()
    #Menambahkan Order
    try:
        sqlQuery="INSERT INTO ordertable (orderno, paket, quantity, status, doo, totalHarga, username, notes) VALUES (%s, %s ,%s, %s ,%s, %s, %s, %s)"
        db_cursor.execute(sqlQuery, (orderno, paket, quantity, status, doo, totalHarga, username, notes))
        db_connection.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        print("Order "+str(orderno)+ " berhasil ditambahkan")
    #pesan berhasil
    skirim={
            'response': 'pesan',
            'status': 'berhasil',
            'orderno': str(orderno)
    }    
    return skirim

def updateCb(jsonData): #memproses request saat melakukan update
    if db_connection.is_connected() == False:
        db_connection.connect()
    orderno=jsonData['orderno']
    paket=jsonData['paket']
    quantity=jsonData['quantity']
    status=jsonData['status']
    username=jsonData['username']
    notes=jsonData['notes']
    totalHarga=jsonData['totalHarga']
    #mengambil data harga sebelumnya
    sqlQuery="SELECT totalHarga from ordertable where orderno=%s"%(
        orderno)
    db_cursor.execute(sqlQuery)
    data=db_cursor.fetchone()[0]
    prevHarga=int(data)
    #mengambil saldo saat ini
    try:
        sqlQuery="SELECT saldo from usertable where username='%s'"%(
            username)
        db_cursor.execute(sqlQuery)
        prevsaldo=int(db_cursor.fetchone()[0])
        saldo=prevsaldo-int(totalHarga)+prevHarga
        if (saldo<0):
            skirim={
                'response': 'update',
                'status' : 'saldo kurang'
            }
            print("saldo kurang")
            return skirim
        #update saldo
        sqlQuery="Update usertable set saldo=%s where username='%s'" %(
            saldo, username)
        db_cursor.execute(sqlQuery)
        db_connection.commit()
        #update ordertable
        #db_cursor.execute("use ordertable")
        sqlQuery="Update ordertable set paket='%s', quantity='%s', status='%s', username='%s', totalHarga='%s', notes='%s' where orderno=%s" %(
            paket, quantity, status, username, totalHarga, notes, orderno)
        db_cursor.execute(sqlQuery)
        db_connection.commit()
    except:
        skirim={
        'response': 'update',
        'status' : 'gagal'
        }
    else:
        skirim={
            'response': 'update',
            'status' : 'berhasil'
        }
        print("Berhasil update ordertable untuk orderno="+str(orderno))
    return skirim

def deleteCb(jsonData): #memproses request delete order
    orderno=jsonData['orderno']
    #Pastikan data ada
    sqlQuery="SELECT * from ordertable where orderno=%s" %(orderno)
    db_cursor.execute(sqlQuery)
    data=db_cursor.fetchall()
    if (data!=[]):
        sqlQuery="DELETE from ordertable where orderno=%s" %(orderno)
        db_cursor.execute(sqlQuery)
        db_connection.commit()
        print("Berhasil menghapus orderno="+str(orderno))
        skirim={
            'response': 'delete',
            'status': 'berhasil'
        }
    else:
        skirim={
            'response': 'delete',
            'status': 'berhasil',
            'keterangan': 'data tidak ada'
        }
        print ("Gagal menghapus data karena orderno="+str(orderno)+" tidak ada")
    return skirim

def searchCb(jsonData): #memproses request saat diminta search
    if (jsonData['tipe']=='orderno'):
        orderno=jsonData['orderno']
        sqlQuery="SELECT * from ordertable where orderno=%s" %(orderno)
        db_cursor.execute(sqlQuery)
        data=db_cursor.fetchall()
        skirim={
            'response': 'search',
            'status' : 'berhasil',
            'tipe' : 'orderno',
            'isi' : data
        }
        print("Pencarian orderno="+str(orderno)+" selesai.")
    elif (jsonData['tipe']=='tanggal'):
        tanggal=jsonData['tanggal']
        sqlQuery="SELECT * from ordertable where doo='%s'" %(tanggal)
        db_cursor.execute(sqlQuery)
        data=db_cursor.fetchall()
        skirim={
            'response': 'search',
            'status' : 'berhasil',
            'tipe' : 'tanggal',
            'isi' : data
        }
        print("Pencarian tanggal="+tanggal+" selesai.")
    elif (jsonData['tipe']=='all'):
        sqlQuery="SELECT * from ordertable"
        db_cursor.execute(sqlQuery)
        data=db_cursor.fetchall()
        print(data)
        skirim={
            'response': 'search',
            'status' : 'berhasil',
            'tipe' : 'all',
            'isi' : data
        }
    elif (jsonData['tipe']=='username'):
        username=jsonData['username']
        sqlQuery="Select saldo from usertable where username='%s'" %(username)
        db_cursor.execute(sqlQuery)
        data=db_cursor.fetchone()
        if (data!=None):
            skirim={
                'response': 'search',
                'status' : 'berhasil',
                'tipe' : 'username',
                'isi' : str(data[0])
            }
        else :
            skirim={
                'response': 'search',
                'status' : 'gagal',
                'tipe' : 'username',
                'isi' : ''
            }
        
    else:
        print("Search gagal, tipe tidak terdefinisi")
        skirim={
            'response': 'search',
            'status': 'gagal'
        }
    return skirim
    
def topupCb(jsonData): #memproses request untuk topup
    username=jsonData['username']
    topup=jsonData['topup']
    sqlQuery="SELECT saldo from usertable where username='%s'"%(
        username)
    db_cursor.execute(sqlQuery)
    prevsaldo=int(db_cursor.fetchone()[0])
    if (prevsaldo==None):
        skirim={
            'response' : 'topup',
            'status' : 'gagal',
            'keterangan' : 'username tidak ditemukan'
        }
        return skirim
    saldo=prevsaldo+int(topup)
    #update saldo
    sqlQuery="Update usertable set saldo=%s where username='%s'" %(
        saldo, username)
    db_cursor.execute(sqlQuery)
    db_connection.commit()
    skirim={
            'response' : 'topup',
            'status' : 'berhasil',
            'saldo' : str(saldo)
        }
    return skirim

def showHistory(jsonData): #memproses request untuk update history
    if db_connection.is_connected() == False:
        db_connection.connect()
    username=jsonData['username']
    sqlQuery = "SELECT * FROM ordertable where username='%s' order by cast(orderno as unsigned) " %(username)
    # implement query Sentence
    db_cursor.execute(sqlQuery) 
    data=db_cursor.fetchall()
    skirim={
        'response': 'showHistory',
        'isi' : data,
        'jumlah' : len(data)
    }
    #db_connection.close()
    return skirim

def switchReq(jsonData): #memproses banyaknya request ke fungsi callback masing-masing
    db_cursor.execute("use restaurant")
    if (jsonData["request"]=='register'):
        x=registerCb(jsonData)
    elif(jsonData["request"]=='login'):
        x=loginCb(jsonData)
    elif(jsonData["request"]=='pesan'):
        x=pesanCb(jsonData)
    elif(jsonData["request"]=='update'):
        x=updateCb(jsonData)
    elif(jsonData["request"]=='delete'):
        x=deleteCb(jsonData)
    elif(jsonData["request"]=='search'):
        x=searchCb(jsonData)
    elif(jsonData["request"]=='topup'):
        x=topupCb(jsonData)
    elif(jsonData["request"]=='showHistory'):
        x=showHistory(jsonData)
    else:
        x="Invalid Request Data"
    return x

def multi_threaded_client(connection, address): #fungsi multi threading
    try:
        data = connection.recv(4096)
        file_object=open('logFile.txt', 'a')
        sdata=str(data,'utf-8')
        receiveTime=str(datetime.now())
        
        print("Pesan dari",address[0],":",address[1]," =", sdata)
        jsonData=json.loads(sdata)
        print("jsonData = "+str(jsonData))
        skirim=switchReq(jsonData)
        sendTime=str(datetime.now())
        writeTxt="Client : "+str(address[0])+":"+str(address[1])+"\nR"+receiveTime+"  "+sdata+"\nS"+sendTime+" "+str(skirim)+"\n\n"
        skirim["receiveTime"]=receiveTime
        skirim["sendTime"]=sendTime
        
        file_object.write(writeTxt)
        print("skirim : "+str(skirim))
        connection.sendall(bytes(json.dumps(skirim, sort_keys=True, default=str), 'utf-8'))
    finally:
        connection.close()
        print("koneksi dengan "+address[0]+" ditutup\n")
        file_object.close()

#melakukan akses ke database mysql
db_connection = mysql.connector.connect(
    host=hostSQL,
    user="root",
    password="password",
    auth_plugin='mysql_native_password')
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)

try:
  ServerSideSocket.bind((host, port))
except socket.error as e:
  print(str(e))

print('Socket is listening..'+"PORT="+str(port))
ServerSideSocket.listen(5)

while True:
    Client, address = ServerSideSocket.accept()
    connectionSocket = ssl_wrap_socket(Client, ssl_version, serverkey, serverpem)
    #print('Connected to: ' + address[0] + ':' + str(address[1]))
    if connectionSocket != None:
            print('Connected to :', address[0], ':', address[1])
            # Start a new thread and return its identifier
            start_new_thread(multi_threaded_client, (connectionSocket, address))
    else:
        Client.close()
    
ServerSideSocket.close()
