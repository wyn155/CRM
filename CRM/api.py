from mymain import api
from myuris.searchuri import CustomerAPI
# from myuris.often import often_CustomerAPI


def register_api():
    api.add_resource(CustomerAPI,"/api/customer", endpoint="customer")
    # api.add_resource(often_CustomerAPI,"/api/oftencustomer",endpoint="oftencustomer")
