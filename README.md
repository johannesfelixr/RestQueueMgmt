# RestQueueMgmt
Created by (2021, May 08) :
1. 13217006 Johannes Felix Rimbun
2. 13217018 Ryan Dharma Chandra
3. 13217071 Wilfrid Azariah

This system is provided as queue management in a restaurant so that every customer can order a food in a restaurant without swarm with another customers in order to prevent  Covid-19 Infection.

The demonstration video can be found at demoRestoMgmtDAN.mp4
The report can be found in the report fileRestoMgmtDAN.pdf

There are three programs that must be run, each of which is located in the /server/, /restaurant_client/, and /android/ directories. In addition, the mySQL configuration backup database is also located in the /SQLdatabase/ directory.

To set up the server, do the following steps.
1. Make sure that in the "server preparation" section, the IP Address and Port written are the same as the IP Address on the computer to run this server program. For example, "192.168.100.8".
2. Set the port value. In this project, port=3456 is used.
3. In the "Constant for mySQL" section, make sure that the IP Address written is the same as the IP Address on the computer running the mySQL database. For example, "192.168.100.6".
4. Make sure that the certificates for SSL verification, namely “server.key”, “server.pem”, and “client.pem” are in the same directory as the server.py program.
5. Make sure that the mySQL database has been run first before running this server program.
6. To run this server program, enter the command in the command line: server.py.

To create and run a mySQL database, the following procedures are performed.
1. Make sure Mysql has been installed properly
2. Load the existing database according to the directory. If the database has been loaded successfully, instructions 7 and 10-12 do not need to be executed. Meanwhile, if the database fails to load, follow all instructions.
2. Run [mysqld] on cmd
3. Login to mysql with [mysql -u root -p]
4. Enter password
5. Create a user for the server with [CREATE USER 'root'@'192.168.100.8' IDENTIFIED BY 'root';]
6. Create a database with [CREATE DATABASE restaurant;]
7. Grant server access to database with [GRANT ALL PRIVILEGES ON restaurant.* TO 'root'@'localhost';]
8. Run [Flush privileges;]
9. Run [use restaurant;] to prepare table creation in database
10. Run [create table if not exists ordertable(orderno INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, package VARCHAR(30), quantity VARCHAR(30), status VARCHAR(10), doo date, totalPrice INT(30), username VARCHAR(30), notes VARCHAR(30))AUTO_INCREMENT=1;]
11. Run [create table if not exists usertable(Id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, username VARCHAR(30), password VARCHAR(65), balance INT(30))AUTO_INCREMENT=1;]

To prepare the client at the cashier, do the following steps.
1. Make sure that in the “Socket Configuration” section, the IP Address and Port written are the same as the IP Address on the computer to run the server program. For example, "192.168.100.8".
2. Set the port value. In this project, port=3456 is used.
3. Make sure that the certificates for SSL verification, namely “client.key”, “client.pem”, and “server.pem” are in the same directory as the login.py and main.py programs.
4. Make sure the server program has been run first before running this client program.
5. To run this client program, enter the command in the command line: restaurant_client.py.
6. To set up a client on Android, do the following steps.
7. Open the Android project using Android Studio.
8. In the browser, there is a Constant.java file. In the file, make sure that the server's IP address and port match the IP address written in the server_addr and server_port constants. In this case, we use server_addr=”192.168.100.8” and server_port=3456.
9. To run this application, you can use the menu Run → Run App. Apart from that, this app can also be exported as an APK with Build → Build Bundle(s)/Apk(s) → Build Apk(s) 
