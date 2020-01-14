from flask import Blueprint,render_template

search = Blueprint("search",__name__,url_prefix="/search")

# @search.route("/")
# # def indx():
# #     return render_template("search.html")