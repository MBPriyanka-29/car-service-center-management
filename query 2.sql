/*
drop database car_service_management_system;
create database car_service_management_system;

drop table station_provides_service;
drop table service;
drop table  login_admin;
drop table  login_customer;
drop table  bill;
drop table insurance;
drop table  car;
drop table mechanic;
drop table service_station;
drop table admin;
drop table customer;
drop table pays;

*/

#------------------------------ ADMIN ---------------
create table admin(
admin_id bigint,
a_fname varchar(30) NOT NULL,
a_lname varchar(30),
emailID varchar(100),
primary key(admin_id)
);
#alter table admin AUTO_INCREMENT=200000;
#alter table admin add a_fname varchar(30);
#alter table admin add a_lname varchar(30);
#alter table admin drop column pswd;
#------------------------------ CUSTOMER ---------------
create table customer(
customer_id bigint,
c_fname varchar(30) NOT NULL,
c_lname varchar(30),
dateOfBirth date,
first_address varchar(150) NOT NULL,
district varchar(50) NOT NULL,
state varchar(50) DEFAULT "KARNATAKA",
pincode int(6),
dl_num varchar(16),
phone_num bigint(10),
emailID varchar(100) UNIQUE NOT NULL,
primary key(customer_id),
constraint length_of_customerID_not_equal_to_12 check(length(customer_id)=12),
constraint invalid_pincode check(length(pincode)=6),
constraint invalid_phone_number check(phone_num between 6000000000 and 9999999999)
);
#alter table customer modify column dl_num varchar(16);
#alter table customer AUTO_INCREMENT=400000;

#delete from service where service_id in (100,101,102);
#delete from car where car_name in ('swift dzire','verna','alto');
#delete from login_customer where emailID='priyankamb.cs18@rvce.edu.in';
#------------------------------ login customer ---------------
create table login_customer (
customer_id bigint,
emailID varchar(100) primary key,
pswd varchar(150),
constraint length_of_password_is_less_than_8 check(length(pswd)>=8),
foreign key(customer_id) references customer(customer_id) on delete cascade on update cascade
);
#------------------------------ login admin ---------------
create table login_admin (
admin_id bigint,
emailID varchar(100) primary key,
pswd varchar(150),
constraint length_of_password_should_be_greater_than_8 check(length(pswd)>=8),
foreign key(admin_id) references admin(admin_id) on delete cascade on update cascade
);
#------------------------------ SERVICE STATION ---------------
create table service_station(
station_id bigint AUTO_INCREMENT,
s_name varchar(30) NOT NULL,
first_address varchar(150) NOT NULL,
district varchar(50) NOT NULL,
state varchar(50) DEFAULT "KARNATAKA",
pincode int(6),
admin_id  bigint,
s_num bigint(10),
primary key(station_id),
foreign key(admin_id) references admin(admin_id) on delete cascade on update cascade
);
alter table service AUTO_INCREMENT=500;
#alter table service_station add column s_num bigint(10);

#------------------------------ MECHANIC ---------------
create table mechanic(
mechanic_id bigint AUTO_INCREMENT,
m_fname varchar(30) NOT NULL,
m_lname varchar(30),
phone_num bigint(10),
admin_id bigint,
gender varchar(50),
m_status boolean default false,
primary key(mechanic_id),
foreign key(admin_id) references admin(admin_id) on delete cascade on update cascade
#foreign key(station_id) references service_station(station_id) on delete cascade on update cascade
);
alter table mechanic AUTO_INCREMENT=300000;
#delete from mechanic where m_fname='as';
#alter table mechanic add column m_status int default false;
#alter table mechanic add column gender varchar(50);
#alter table mechanic drop column m_status;

#------------------------------ SERVICE  ---------------
create table service(
service_id bigint AUTO_INCREMENT,
s_name varchar(30) NOT NULL,
#s_type varchar(30),
s_date date,
s_time TIME,
price bigint default 0,
Specifications varchar(200),
delivery_type varchar(50),
address varchar(200) default 'NA',
pincode varchar(50),
admin_remark varchar(200) default 'No action taken yet',
admin_remark_date datetime,
admin_status int default 0,
s_status int default 0,
customer_id bigint,
service_request_date datetime,
admin_id bigint,
primary key(service_id),
foreign key(customer_id) references customer(customer_id) on delete cascade on update cascade,
foreign key(admin_id) references admin(admin_id) on delete cascade on update cascade
);
#alter table service add column admin_id bigint;
#ALTER TABLE service
#ADD FOREIGN KEY (admin_id) REFERENCES admin(admin_id);
alter table service AUTO_INCREMENT=100;
#alter table service drop column s_status;
#alter table service alter address set default 'NA';
#alter table service add column s_status int default 0 ;

#------------------------------ BILL ---------------
create table bill(
bill_id bigint AUTO_INCREMENT,
bill_date date,
bill_time time,
service_amount float NOT NULL,
additional_parts float,
other_amount float,
tax float,
discount float,
final_amount float NOT NULL,
status bool,
primary key(bill_id)
);
alter table bill AUTO_INCREMENT=21000;
#------------------------------ CAR ---------------
create table car(
car_name varchar(50),
company varchar(50),
model varchar(50),
#model_year int,
#car_type varchar(50),
Registration_num varchar(50),
customer_id bigint,
mechanic_id bigint,
primary key(Registration_num,customer_id),
foreign key(customer_id) references customer(customer_id) on delete cascade on update cascade,
foreign key(mechanic_id) references mechanic(mechanic_id) on delete cascade on update cascade
);
#drop table car;
#alter table car AUTO_INCREMENT=10000000;
#alter table car add column Registration_num varchar(50);
#alter table car drop column Liscence_num;
#delete from car where car_name='swift dzire';
#delete from service where s_name='FullService';
#------------------------------ INSURANCE ---------------
create table insurance(
insurance_id bigint AUTO_INCREMENT,
premium_amount float,
renewal_Date date,
Registration_num varchar(50),
customer_id bigint,
primary key(insurance_id),
foreign key(Registration_num ,customer_id) references car(Registration_num,customer_id) on delete cascade on update cascade
#foreign key(customer_id) references customer(customer_id) on delete cascade on update cascade
);
alter table insurance AUTO_INCREMENT=3000;

#------------------------------ CAR SERVICE ---------------
create table car_claims_service(
service_id bigint,
Registration_num varchar(50),
customer_id bigint,
primary key(Registration_num,service_id),
foreign key(Registration_num,customer_id) references car(Registration_num,customer_id) on delete cascade on update cascade,
foreign key(service_id) references service(service_id) on delete cascade on update cascade
);
#drop table car_claims_service;


#------------------------------ STATION SERVICE ---------------
create table station_provides_service(
station_id bigint,
service_id bigint,
primary key(station_id,service_id)
);

#------------------------------ PAYS ---------------
create table pays(
customer_id bigint,
service_id bigint,
admin_id bigint,
bill_id bigint,
primary key(bill_id),
foreign key(service_id) references service(service_id) on delete cascade on update cascade,
foreign key(customer_id) references customer(customer_id) on delete cascade on update cascade,
foreign key(admin_id) references admin(admin_id) on delete cascade on update cascade
);