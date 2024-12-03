from flask import request

class CustomerForm:
    def __init__(self):
        self.id = request.form.get('customer_id')
        self.customer_unique_id = request.form.get('customer_unique_id')
        self.customer_name = request.form.get('customer_name')
        self.customer_zip_code = request.form.get('customer_zip_code')
        self.customer_city = request.form.get('customer_city')
        self.customer_state = request.form.get('customer_state')
    

