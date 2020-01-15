from flask_restful import Resource,fields
from model import Crm_contact,Crm_cautions,Customer
from myblueprints.search_blueprints import search
from flask import render_template,request,redirect
import json

# 返回资源


class CustomerAPI(Resource):
    @search.route("/", methods=["GET", "POST"])
    def get(self):
        customer_code = request.args.get("customer_code")
        name = request.args.get('customer_name','NONE')


        data = []
        con = []
        data_code = Customer.query.filter_by(customer_code = 20615).all()
        data_name = Customer.query.filter(Customer.customer_name.like("%"+name+"%")).all()

        data.append(data_name)
        data.append(data_code)
        for item in data:
            for i in item:
                d = i.__dict__
                d.pop('_sa_instance_state')
                con.append(d)


        return {'code':200,'msg':'ok','data':con}
        # return json.dumps({'code':200,'msg':'ok','data':con})


# 常用客户 ['滴滴','联影','大华','韶音','蚂蚁']
# def regular_customers(self):
#     clien_to = ['滴滴','联影','大华','韶音','蚂蚁']
#     data_code = Customer.query.filter_by('{}').all().format(clien_to)
#     print(data_code)
#
#     return {'data' : data_code}