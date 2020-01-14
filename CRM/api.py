from mymain import api
from myuris.searchuri import CrmcontactAPI


def register_api():
    api.add_resource(CrmcontactAPI,"/api/contact", endpoint="contact")
