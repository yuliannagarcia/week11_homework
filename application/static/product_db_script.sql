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

insert into product (productName, productDescription, productPrice) values
('Handbag2', 'Stylish leather handbag with multiple compartments', 149.99),
('Watch', 'Elegant wristwatch with stainless steel strap', 49.99),
('Sunglasses', 'UV protection sunglasses with polarized lenses', 29.99),
('Scarf', 'Soft cashmere scarf in a variety of colors', 39.99),
('Wallet2', 'Slim leather wallet with RFID blocking technology', 19.99);

insert into product (productName, productDescription, productPrice) values
('Backpack', 'Durable nylon backpack with padded laptop compartment', 79.99),
('Earrings', 'Sparkling diamond earrings in various styles', 149.99),
('Phone Case', 'Slim protective phone case with shock-absorbent design', 9.99),
('Necklace', 'Trendy statement necklace with adjustable chain', 59.99),
('Shoes', 'Comfortable running shoes with breathable mesh upper', 89.99),
('Belt', 'Genuine leather belt with classic buckle design', 34.99),
('Hat', 'Stylish fedora hat made from premium wool felt', 44.99),
('Gloves', 'Warm knit gloves with touchscreen compatibility', 19.99),
('Perfume', 'Luxurious fragrance with floral and woody notes', 69.99),
('Notebook', 'Sleek leather-bound notebook for jotting down ideas', 24.99);