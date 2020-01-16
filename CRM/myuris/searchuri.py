from flask_restful import Resource,fields
from model import Crm_contact,Crm_cautions,Customer
from myblueprints.search_blueprints import search
from flask import render_template,request,redirect
import json

# 返回资源
@search.route("/")
def index():
    return render_template("search.html")


class CustomerAPI(Resource):
    @search.route("/search", methods=["GET", "POST"])
    def get(self):
        customer_code = request.args.get("customer_code")
        print(customer_code)
        name = request.args.get("customer_name","NONE")


        data = []
        con = []
        data_code = Customer.query.filter_by(customer_code = customer_code).all()
        # data_name = Customer.query.filter(Customer.customer_name.like("%"+name+"%")).all()
        # data.append(data_name)
        data.append(data_code)
        for item in data:
            for i in item:
                d = i.__dict__
                d.pop("_sa_instance_state")
                # d = str(d)
                print(d)
                # d = json.loads(d)
                con.append(d)


        return {'code':200,'msg':'ok','data':con}
        # return json.dumps({'code':200,'msg':'ok','data':con})


