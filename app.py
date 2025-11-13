from flask import Flask, jsonify, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello from Pet adoption\n'

@app.route("/meow")
def cat():
    return "meow\n"

@app.route("/user/profile/<username>")
def show_user_profile(username):
    return f"User {escape(username)}\n"

@app.route("/post/<int:post_id>")
def show_post_with_int(post_id):
    return f"Post {post_id}\n"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath {escape(subpath)}\n"

@app.route("/user/login/<string:user_name>")
def user_login(user_name):
    return f"welcome back {user_name}\n"

@app.route("/test_json")
def show_json():
    x = "test1"
    y = "test2"
    return jsonify(a=x, z=y)
# enter a 128 bit identifier writen in the standard 36 bit character text format in the browser
@app.route("/item/<uuid:item_128bit>")
def show_uuid_with_json(item_128bit):
    return jsonify({"item_id": str(item_128bit)})

@app.route("/thing/<uuid:first_thing>")
def show_uuid(first_thing):
    return f"show 128 bit of {first_thing}\n"

@app.route("/user/<float:account_balance>")
def show_account_balance(account_balance):
    return f"Current Account balance without line of credit: {account_balance}"

@app.route("/projects/")
def projects():
    return "The project page"

@app.route("/about")
def about():
    return "The about page\n"


with app.test_request_context():
    print(url_for("index"))
    print(url_for("show_user_profile", username="Arnold"))
    print(url_for("about", next="/"))

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="127.0.0.1")