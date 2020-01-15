from mymain import db

class Crm_contact(db.Model):
    __tablename__ = "crm_contact"
    customer_code = db.Column(db.Integer,db.ForeignKey("customer.customer_code"))
    name = db.Column(db.String(100),primary_key=True)
    position = db.Column(db.String(100))
    appellation = db.Column(db.String(100))
    contact_information = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    remarks = db.Column(db.Text)

class Crm_cautions(db.Model):
    __tablename__ = "crm_cautions"
    customer_code = db.Column(db.Integer,db.ForeignKey("customer.customer_code"))
    matters_attention = db.Column(db.Text)
    modifier = db.Column(db.String(100),primary_key=True)
    modification_time = db.Column(db.TIMESTAMP)

class Customer(db.Model):
    __tablename__ = "customer"
    customer_code = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.Text)
    customer_shortname = db.Column(db.Text)

