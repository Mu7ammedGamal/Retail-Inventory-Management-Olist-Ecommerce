from app import db


class Customer(db.Model):
    __tablename__ = 'customers'  # The name of your table in the database

    customer_id = db.Column("customer_id",db.String(50), primary_key=True)  # nvarchar(50), unchecked
    customer_unique_id = db.Column("customer_unique_id",db.String(50), nullable=False)  # nvarchar(50), checked
    customer_name = db.Column("customer_name",db.String(50), nullable=False)  # nvarchar(50), checked
    customer_zip_code = db.Column("customer_zip_code",db.Integer, nullable=False)  # int, checked
    customer_city = db.Column("customer_city",db.String(50), nullable=False)  # nvarchar(50), checked
    customer_state = db.Column("customer_state",db.String(50), nullable=False)  # nvarchar(50), checked


    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id}, customer_name={self.customer_name})>"
