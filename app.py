from flask import (jsonify, url_for, redirect,
                   render_template, request,
                   abort, Flask, flash)
# flask_login does not handle password hashing or database storage
from flask_login import login_required, LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Pet, User
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret123"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    pets = Pet.query.all()
    users = User.query.all()
    return render_template("index.html", pets=pets, users=users) # render the child who inherits from the parent

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("index"))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for("index"))



@app.route("/add-pet", methods=['GET', 'POST'])
def add_pet(): # used within the html using jinja patterns {{}} submits the form
    if request.form: # if there is no form that's been submitted
        new_pet = Pet(name=request.form['name'], age=request.form['age'],
                      breed=request.form['breed'], color=request.form['color'],
                      size=request.form['size'], weight=request.form['weight'],
                      url=request.form['url'], url_tag=request.form['alt'],
                      pet_type=request.form['pet'], gender=request.form['gender'],
                      spay=request.form['spay'], house_trained=request.form['housetrained'],
                      description=request.form['description'])
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('index'))# redirect the user to the homepage after adding a pet
    return render_template("addpet.html")

# update to accept the id variable and enter the image from the url href of jinja and url_for module in the index.html file
# how to pass information from one page to another without using a new route/view
@app.route("/pet/<id>") # use the id to fint the pet and sent it to the template
def pet(id): # 127.0.0.1:8000/pet/1
    pet = Pet.query.get_or_404(id)
    return render_template("pet.html", pet=pet)
    

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_pet(id):
    pet = Pet.query.get_or_404(id)
    if request.form:
        pet.name = request.form['name']
        pet.age = request.form['age']
        pet.breed = request.form['breed']
        pet.color = request.form['color']
        pet.size = request.form['size']
        pet.weight = request.form['weight']
        pet.url = request.form['url']
        pet.url_tag = request.form['alt']
        pet.name = request.form['name']
        pet.pet_type = request.form['pet']
        pet.gender = request.form['gender']
        pet.spay = request.form['spay']
        pet.house_trained = request.form['housetrained']
        pet.description = request.form['description']
        db.session.commit()
        return redirect(url_for("index")) # redirect afterwards to homepage
    return render_template("editpet.html", pet=pet)



# the route deletes any id. it requires authentication, login manager
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_pet(id):
    pet = Pet.query.get_or_404(id) #flask sqlalchemy queries for views
    # current_user is a proxy from flask
    if not pet.helper_function_check_deletion_permission(current_user): # typing in the browser /delete/1 will permanently delete the object with id 1
        abort(403)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for("index")) # redirect to homepage aftwerwards action


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", msg=error), 404
    

if __name__ == "__main__":
    # use a proxy
    with app.app_context(): # keeps track of application-level data throughout the app during a request, a command-line command, or else...
        db.create_all()
    app.run(debug=True, port=8000, host="127.0.0.1")