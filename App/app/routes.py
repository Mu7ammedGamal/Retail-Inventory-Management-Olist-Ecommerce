from flask import Blueprint,render_template,request,redirect,url_for
from app import db
from app.models import Customer
from app.forms import CustomerForm
from app.data_loader import load_data,load_olist_data

main = Blueprint('main',__name__)
@main.route('/',methods=['POST','GET'])
def home():
   if request.method == 'POST':
     # Retrieve Form data
        form = CustomerForm()
        
        new_customer = Customer(customer_id = form.id,
                                customer_unique_id = form.customer_unique_id,
                                customer_name=form.customer_name,
                                customer_zip_code=form.customer_zip_code,
                                customer_city =form.customer_city,
                                customer_state =form.customer_state )
        db.session.add(new_customer) # add new customer)
        db.session.commit()         # save Changes
        return redirect(url_for('main.home'))
   return render_template('home.html')    
@main.route('/dataframes')
def display_dataframes():
    df_customers,df_geolocation,df_orderitem,df_payment,df_reviews,df_orders,df_products,df_seller,olist_data = load_data()

    customer_html = df_customers.to_html(classes='data',header=True,index=False)
    geolocation_html = df_geolocation.to_html(classes='data',header=True,index=False)
    orderitem_html = df_orderitem.to_html(classes='data',header=True,index=False)
    payment_html = df_payment.to_html(classes='data',header=True,index=False)
    reviews_html = df_reviews.to_html(classes='data',header=True,index=False)
    order_html = df_orders.to_html(classes='data',header=True,index=False)
    product_html = df_products.to_html(classes='data',header=True,index=False)
    seller_html = df_seller.to_html(classes='data',header=True,index=False)
    olist_html = olist_data.to_html(classes='data',header=True,index=False)
    
         
    return render_template('dataframes.html',customers=customer_html,geolocation=geolocation_html,
                           orderitem=orderitem_html,payment=payment_html,reviews=reviews_html,
                           orders=order_html,products=product_html,sellers=seller_html,olist=olist_html)
