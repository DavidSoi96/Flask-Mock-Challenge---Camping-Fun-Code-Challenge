from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Signup(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    time = db.Column(db.Integer)
    
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    @validates('time')
    def validate_time(self, key, hour):
        if not isinstance(hour, int) or not (0 <= hour <= 23):
            raise ValueError("Time must be between 0 and 23")
        return hour


class Camper(db.Model):
    __tablename__ = 'campers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name

    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or not (8 <= age <= 18):
            raise ValueError("Age must be between 8 and 18")
        return age


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
