from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

from config import db, bcrypt
from flask_bcrypt import Bcrypt
bycrpt = Bcrypt()

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-_password_hash', '-recipes.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # Relationship
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        return username



class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    serialize_rules = ('-user.recipes',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required')
        return title
    
    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions:
            raise ValueError('Instructions are required')
        if len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters long')
        return instructions
    

