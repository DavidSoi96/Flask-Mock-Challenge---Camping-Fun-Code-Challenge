from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"errors": [str(e)]}), 400


# Campers CRUD
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
            "activity_id": s.activity_id,
            "activity": {
                "id": s.activity.id,
                "name": s.activity.name,
                "difficulty": s.activity.difficulty
            }
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


@app.route("/campers/<int:id>", methods=["PATCH"])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    
    data = request.json
    try:
        if "name" in data:
            camper.name = data["name"]
        if "age" in data:
            camper.age = data["age"]
        db.session.commit()
        return jsonify({"id": camper.id, "name": camper.name, "age": camper.age}), 202
    except ValueError as e:
        return handle_value_error(e)


@app.route("/campers/<int:id>", methods=["DELETE"])
def delete_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    
    db.session.delete(camper)
    db.session.commit()
    return "", 204


# Activities CRUD
@app.route("/activities", methods=["GET"])
def get_activities():
    activities = Activity.query.all()
    return jsonify([{"id": a.id, "name": a.name, "difficulty": a.difficulty} for a in activities])


@app.route("/activities", methods=["POST"])
def create_activity():
    data = request.json
    try:
        activity = Activity(name=data.get("name"), difficulty=data.get("difficulty"))
        db.session.add(activity)
        db.session.commit()
        return jsonify({"id": activity.id, "name": activity.name, "difficulty": activity.difficulty}), 201
    except (ValueError, KeyError) as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route("/activities/<int:id>", methods=["PATCH"])
def update_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    data = request.json
    try:
        if "name" in data:
            activity.name = data["name"]
        if "difficulty" in data:
            activity.difficulty = data["difficulty"]
        db.session.commit()
        return jsonify({"id": activity.id, "name": activity.name, "difficulty": activity.difficulty}), 202
    except (ValueError, KeyError) as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route("/activities/<int:id>", methods=["DELETE"])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return "", 204


# Signups CRUD
@app.route("/signups", methods=["GET"])
def get_signups():
    signups = Signup.query.all()
    return jsonify([{
        "id": s.id,
        "time": s.time,
        "camper_id": s.camper_id,
        "activity_id": s.activity_id,
        "camper": {
            "id": s.camper.id,
            "name": s.camper.name,
            "age": s.camper.age
        },
        "activity": {
            "id": s.activity.id,
            "name": s.activity.name,
            "difficulty": s.activity.difficulty
        }
    } for s in signups])


@app.route("/signups/<int:id>", methods=["GET"])
def get_signup(id):
    signup = Signup.query.get(id)
    if not signup:
        return jsonify({"error": "Signup not found"}), 404
    
    return jsonify({
        "id": signup.id,
        "time": signup.time,
        "camper_id": signup.camper_id,
        "activity_id": signup.activity_id,
        "camper": {
            "id": signup.camper.id,
            "name": signup.camper.name,
            "age": signup.camper.age
        },
        "activity": {
            "id": signup.activity.id,
            "name": signup.activity.name,
            "difficulty": signup.activity.difficulty
        }
    })


@app.route("/signups", methods=["POST"])
def create_signup():
    data = request.json
    try:
        camper = Camper.query.get(data["camper_id"])
        activity = Activity.query.get(data["activity_id"])
        
        if not camper:
            return jsonify({"errors": ["Camper not found"]}), 404
        if not activity:
            return jsonify({"errors": ["Activity not found"]}), 404
        
        signup = Signup(
            camper_id=data["camper_id"],
            activity_id=data["activity_id"],
            time=data["time"]
        )
        db.session.add(signup)
        db.session.commit()
        
        return jsonify({
            "id": signup.id,
            "time": signup.time,
            "camper_id": signup.camper_id,
            "activity_id": signup.activity_id,
            "camper": {
                "id": camper.id,
                "name": camper.name,
                "age": camper.age
            },
            "activity": {
                "id": activity.id,
                "name": activity.name,
                "difficulty": activity.difficulty
            }
        }), 201
    except (ValueError, KeyError) as e:
        if isinstance(e, ValueError):
            return handle_value_error(e)
        else:
            return jsonify({"errors": [str(e)]}), 400


@app.route("/signups/<int:id>", methods=["DELETE"])
def delete_signup(id):
    signup = Signup.query.get(id)
    if not signup:
        return jsonify({"error": "Signup not found"}), 404
    
    db.session.delete(signup)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)