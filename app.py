from flask import Flask, request, jsonify
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)
from marshmallow import ValidationError

app = Flask(__name__)
import os
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" if os.environ.get("TESTING") else "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# --- Workouts ---

@app.route("/workouts", methods=["GET"])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 422
    try:
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200


# --- Exercises ---

@app.route("/exercises", methods=["GET"])
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 422
    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Exercise name already exists."}), 422
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200


# --- Workout Exercises ---

@app.route("/workout_exercises", methods=["POST"])
def add_exercise_to_workout():
    try:
        data = workout_exercise_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 422

    if not db.session.get(Workout, data["workout_id"]):
        return jsonify({"error": "Workout not found"}), 404
    if not db.session.get(Exercise, data["exercise_id"]):
        return jsonify({"error": "Exercise not found"}), 404

    try:
        we = WorkoutExercise(**data)
        db.session.add(we)
        db.session.commit()
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    return jsonify(workout_exercise_schema.dump(we)), 201


if __name__ == "__main__":
    app.run(debug=True)
