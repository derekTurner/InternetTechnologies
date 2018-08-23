import sqlite3

conn = sqlite3.connect('Payroll.db')
conn.execute('create table employee(id integer primary key,'+
			 'name varchar(20),notes varchar(100),rvv integer)')
conn.execute('create table post(empid references employee,efrom date, '+  
			'grade varchar(4),manager references employee,rvv integer)')
conn.execute('create table holiday(empid references employee,hfrom date,'+  
			' hto date, agreed date,rvv integer)')
conn.execute('create table rvv(seq integer)')
conn.execute('create table user(uname varchar(20) primary key,password varchar(20))')
conn.execute("insert into employee values(1562,'Johnathan Black','Sales',1)")
conn.execute("insert into employee values(1567,'Mary White','Finance',2)")
conn.execute("insert into employee values(1569,'Paul Green','HR',3)")
conn.execute("insert into post values(1562,'2017-02-01','A1',1569,4)")
conn.execute("insert into post values(1562,'2017-04-01','A2',null,5)")
conn.execute("insert into post values(1567,'2017-02-01','B1',1569,6)")
conn.execute("insert into post values(1569,'2017-02-01','A2',null,7)")
conn.execute("insert into holiday values(1567,'2017-03-02','2017-03-07'," + 
			"'2017-02-05',8)")
conn.execute("insert into holiday values(1569,'2017-04-04','2017-04-18'," + 
			"null,9)")
conn.execute("insert into rvv values(10)")
conn.execute("insert into user values('aUser','whosOk')")
conn.commit()
print('Done')
