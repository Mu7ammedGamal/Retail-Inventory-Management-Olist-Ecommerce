CREATE TABLE customers_data (
    customer_id VARCHAR(255) ,
    customer_unique_id VARCHAR(255) ,
    customer_zip_code_prefix INT ,
    customer_city VARCHAR(50) ,
    customer_state VARCHAR(50) ,
    PRIMARY KEY (customer_id)
);

CREATE TABLE orders_data (
    order_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    order_status VARCHAR(255) NOT NULL,
    order_purchase_timestamp DATETIME NOT NULL,
    order_approved_at DATETIME NOT NULL,
    order_delivered_carrier_date DATETIME NOT NULL,
    order_delivered_customer_date DATETIME NOT NULL,
    order_estimated_delivery_date DATETIME NOT NULL,
    PRIMARY KEY (order_id),
	FOREIGN KEY (customer_id) REFERENCES customers_data (customer_id)
);


CREATE TABLE order_payment_data (
    order_id VARCHAR(255) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(50) ,
    payment_installments INT ,
    payment_value FLOAT,
    
    );

CREATE TABLE seller_data (
    seller_id VARCHAR(255) ,
    seller_zip INT ,
    seller_city VARCHAR(50) ,
    seller_state VARCHAR(50),
   
    PRIMARY KEY (seller_id)
);

CREATE TABLE product_category_data (
    product_category_name VARCHAR(255) ,
    product_category_name_english VARCHAR(255) ,

    PRIMARY KEY (product_category_name)
);

CREATE TABLE products_data (
    product_id VARCHAR(255) ,
    product_category_name VARCHAR(255) NOT NULL,
    product_photos_qty FLOAT ,
    product_description_length INT,
    product_weight_g INT ,
    product_length_cm INT ,
    product_height_cm INT,
    product_width_cm INT ,

    FOREIGN KEY (product_category_name) REFERENCES product_category_data (product_category_name),
    PRIMARY KEY (product_id)
);

CREATE TABLE order_item_data (
    order_id VARCHAR(255) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    seller_id VARCHAR(255) NOT NULL,
    shipping_limit_date DATETIME NOT NULL,
    price FLOAT NOT NULL,
    freight_value FLOAT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_data (product_id),
    FOREIGN KEY (seller_id) REFERENCES seller_data (seller_id),
    FOREIGN KEY (order_id) REFERENCES orders_data (order_id),
);


CREATE TABLE state_name (
    state_full_name VARCHAR(50) NOT NULL,
    state_abbreviation VARCHAR(50) NOT NULL,
	PRIMARY KEY (state_abbreviation)

);
