from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


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


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"errors": [str(e)]}), 400



@app.route("/campers", methods=["GET"])
def get_campers():
    campers = Camper.query.all()
    return jsonify([{"id": c.id, "name": c.name, "age": c.age} for c in campers])


@app.route("/campers/<int:id>", methods=["GET"])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify({
        "id": camper.id,
        "name": camper.name,
        "age": camper.age,
        "signups": [{
            "id": s.id,
            "time": s.time,
            "camper_id": s.camper_id,
            "activity_id": s.activity_id
        } for s in camper.signups]
    })



@app.route("/campers", methods=["POST"])
def create_camper():
    data = request.json
    try:
        camper = Camper(name=data.get("name"), age=data.get("age"))
        db.session.add(camper)
        db.session.commit()
        return jsonify({"id": camper.id, "name": camper.name, "age": camper.age}), 201
    except ValueError as e:
        return handle_value_error(e)
