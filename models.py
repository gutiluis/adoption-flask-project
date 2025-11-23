from flask_login import UserMixin
import datetime
from flask_sqlalchemy import SQLAlchemy
from extensions import db



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('Created', db.DateTime, default=datetime.datetime.now)
    name = db.Column('Name', db.String())
    age = db.Column('Age', db.String())
    breed = db.Column('Breed', db.String())
    color = db.Column('Color', db.String())
    size = db.Column('Size', db.String())
    weight = db.Column('Weight', db.String())
    url = db.Column('URL', db.String())
    url_tag = db.Column("Alt Tag", db.String())
    pet_type = db.Column('Pet Type', db.String())
    gender = db.Column('Gender', db.String())
    spay = db.Column('Spay', db.String())
    house_trained = db.Column('House Trained', db.String())
    description = db.Column('Description', db.Text())
    # check user ownership
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", back_populates="pets")

    def helper_function_check_deletion_permission(self, user):
        return self.owner_id == user.id


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # hashed in production

    # one-to-many relationship: a user has many pets
    pets = db.relationship("Pet", back_populates="owner", cascade="all, delete-orphan")



    def __repr__(self):
        return f'''<Pet (Name: {self.name}
                Age: {self.age}
                Breed: {self.breed}
                Color: {self.color}
                Size: {self.size}
                Weight: {self.weight}
                URL: {self.url}
                Tag: {self.tag}
                Gender: {self.gender}
                Spay: {self.spay}
                House Trained: {self.house_trained}
                Description: {self.description})'''