# data_logger_server
## 1st step:
You can use an existing programming environment for working in Django, or create a new one. We’ll call our env, once it’s created you can activate it:
```bash	
	$ python3 -m venv env 
	$ . env/bin/activate
```
 
now we have to install the requirement using the command bellow 
```bash	
	$ pip3 install -r requirements.txt 
```
## 2nd step:
we have to install some packages that we are going to use on our code 
```bash
	$ sudo apt-get install rabbitmq-server
	$ sudo apt install python3-dev 
	$ sudo apt install python3-dev libmysqlclient-dev default-libmysqlclient-dev
```
## 3rd step: (Mysql Database)
Log in via the MySQL root with the following command:
```bash
	$ sudo mysql -u root
```
We’ll know we are in the MySQL server when our prompt changes to : 
```bash	
	mysql>
```
create a database in MySQL run the following command: 
```mysql
	CREATE DATABASE modbus_db;
```
We are going to create this account, set a password, and grant access to the database we created.  
We can do this by typing the following command:
```mysql
	CREATE USER 'mysql_admin'@'%' IDENTIFIED WITH mysql_native_password BY 'q1w2e3r4';
```	
Next, let the database know that our Django user should have complete access to the database we set up:
```mysql
	GRANT ALL ON modbus_db.* TO 'mysql_admin'@'%';
```
ou now have a database and user account, each made specifically for Django.  
We need to flush the privileges so that the current instance of MySQL knows about the recent changes we’ve made:
```mysql
	FLUSH PRIVILEGES;
```
Next, let’s edit the config file so that it has your MySQL credentials. Use nano as sudo to edit the file and add the following information:
```bash
	$ sudo nano /etc/mysql/my.cnf
```
Add the following lines and include your relevant information (the data base, the user and the password created before)
 
	...
	[client]
	database = modbus_db
	user = mysql_admin
	password = q1w2e3r4
	default-character-set = utf8	
 
 
Once the file has been edited, we need to restart MySQL for the changes to take effect.
```bash	
	$ sudo systemctl daemon-reload
	$ sudo systemctl restart mysql
``` 
 
We need to verify that the configurations in Django detect your MySQL server properly. 
We can do this by running the server. If it fails, it means that the connection isn’t working properly. Otherwise, the connection is valid.  
Let’s first apply our changes to Django with the following:
```bash	
	$ python3 manage.py makemigrations
	$ python3 manage.py migrate
```

With migrations complete, we should verify the successful generation of the MySQL tables that we’ve created via our Django models.
```bash
	$ mysql modbus_db -u mysql_admin
```
Now, select our database modbus_db 
```mysql
	USE modbus_db
```
 
Among the tables are blogsite_comment and blogsite_post. These are the models that we’ve just made ourselves. Let’s validate that they contain the fields we’ve defined.
```mysql
 
	mysql> show tables ;
 
	OUTPUT :
		+-------------------------------------+
		| Tables_in_modbus_db                 |
		+-------------------------------------+
		| auth_group                          |
		| auth_group_permissions              |
		| auth_permission                     |
		| auth_user                           |
		| auth_user_groups                    |
		| auth_user_user_permissions          |
		| django_admin_log                    |
		| django_celery_beat_clockedschedule  |
		| django_celery_beat_crontabschedule  |
		| django_celery_beat_intervalschedule |
		| django_celery_beat_periodictask     |
		| django_celery_beat_periodictasks    |
		| django_celery_beat_solarschedule    |
		| django_celery_results_taskresult    |
		| django_content_type                 |
		| django_migrations                   |
		| django_session                      |
		| slaves_app_memoryzone               |
		| slaves_app_memoryzonehistory        |
		| slaves_app_setting                  |
		| slaves_app_slave                    |
		+-------------------------------------+
		21 rows in set (0.00 sec)
```

let is check that the data base contains the slaves app slave information we run this mysql command :
```mysql
	mysql> DESCRIBE slaves_app_slave ;
 
	OUTPUT:
		+---------------+--------------+------+-----+---------+-------+
		| Field         | Type         | Null | Key | Default | Extra |
		+---------------+--------------+------+-----+---------+-------+
		| slave_address | int(11)      | NO   | PRI | NULL    |       |
		| name          | varchar(100) | NO   |     | NULL    |       |
		| enable        | tinyint(1)   | NO   |     | NULL    |       |
		| mac           | varchar(50)  | NO   |     | NULL    |       |
		| setting_id    | int(11)      | NO   | UNI | NULL    |       |
		+---------------+--------------+------+-----+---------+-------+
		5 rows in set (0.00 sec)
```
## 4th step: (run servers)
Now we will run django-server, celery-server and the periodic task by executing one script shell:
```bash
	$ cd start_server
	$ ./init_script.sh
```
Note: if you have any problem with the module django-rest-swagger. you have to install manually with this command :
```bash
	$ pip3 install django-rest-swagger
```
 
## 5th  step : (testing)
to be sure that everyting is working you have to run this command
 
```bash
	$ cd ~
	$ python3 ~/data_logger_server/unit_tests
```
this script will automate those steps bellow:  
1 - the creation of two slaves, the first with id 1, and the second with id 2.  
2 - the creation of two memory zones , the first one is linked with the first slave , and the second with the second slave.  
3 - we will wait for 31 seconds to wait for the celery server to read the first value from the two slaves , because we are reading values every 15 seconds.  
4 - it will show the values read from the two slaves.  
