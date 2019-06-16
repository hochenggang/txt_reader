# coding=utf-8
from flask import Flask

app = Flask(__name__)

from api.user import api_of_user
app.register_blueprint(api_of_user,url_prefix='/api/user')

from api.book import api_of_book
app.register_blueprint(api_of_book,url_prefix='/api/book')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)

