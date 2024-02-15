create table users( id integer primary key AUTOINCREMENT, email text not null, password text not null);


create table emp ( empid integer primary key AUTOINCREMENT, name text not null, designation text ,Education text not null,email text, phone integer, address text, joining_date timestamp DEFAULT CURRENT_TIMESTAMP,  total_projects integer, years_of_experience integer);