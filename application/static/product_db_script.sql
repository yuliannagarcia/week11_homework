create database 
product_db;

use product_db;

create table product (
id int auto_increment primary key,
ProductName varchar(55) not null,
ProductDescription text,
ProductPrice float not null
);


DELIMITER //

create procedure insertProduct(
in productname varchar(55),
in productDescription text,
in productPrice float
)
begin
insert into product(
productName, productDescription, productPrice)
values 
(productName, productDescription, productPrice);
end // 

call insertProduct ('handbag', 'Gucci', '99.99');

select * from product;
