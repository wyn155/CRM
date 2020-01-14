from flask_restful import Resource,fields
from model import Crm_contact,Crm_cautions
from myblueprints.search_blueprints import search
from flask import render_template,request,redirect
# 返回资源

class CrmcontactAPI(Resource):
    @search.route("/",methods = ["GET","POST"])
    def get(self):
        print(123)
        """
        :param
        """
        con = []
        data = Crm_contact.query.all()
        for item in data:
            item = item.__dict__
            item.pop('_sa_instance_state')
            con.append(item)
        return {'code':200,'msg':'123','data':con}