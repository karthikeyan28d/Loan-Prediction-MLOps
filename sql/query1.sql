select * from customers_train as cust
left join dbo.defaulters as def on cust.ID = def.ID


select * into customers_test from customers_train 
select * into defaulters_test from defaulters 

truncate table customers_test
truncate table defaulters_test

select * from customers_test

alter table defaulters_test
add last_update BIGINT IDENTITY	(1,1)

create table waterTable(id bigint not null)

select * from dbo.runs

select top 10 * from Silver.silver_customers--- customers_train

select * from dbo.customers_train as cust
left join dbo.defaulters as def on cust.ID = def.ID