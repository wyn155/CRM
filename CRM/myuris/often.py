from flask_restful import Resource,fields
from model import Crm_contact,Crm_cautions,Customer
from myblueprints.search_blueprints import search
from flask import render_template,request,redirect
import json
from db import mysql

class often_CustomerAPI(Resource):
    # @search.route("/customer", methods=["GET", "POST"])
    def get(self):
        clien_to = ['滴滴', '联影', '大华', '韶音', '蚂蚁']
        for i in clien_to:
            str = "select customer_code,customer_name,customer_shortname from customer where customer_shortname = '{}'".format(i)
            often_data = mysql.query(str)
            print(often_data)
        return {"data":often_data}