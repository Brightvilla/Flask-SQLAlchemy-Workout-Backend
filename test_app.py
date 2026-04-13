import pytest
import os
os.environ["TESTING"] = "1"
from app import app
from models import db, Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.drop_all()
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


# --- Workout Tests ---

def test_get_workouts_empty(client):
    res = client.get("/workouts")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_workout(client):
    res = client.post("/workouts", json={"name": "Leg Day", "description": "Lower body"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Leg Day"
    assert data["description"] == "Lower body"


def test_create_workout_missing_name(client):
    res = client.post("/workouts", json={"description": "No name"})
    assert res.status_code == 422


def test_create_workout_blank_name(client):
    res = client.post("/workouts", json={"name": "  "})
    assert res.status_code == 422


def test_get_workout_by_id(client):
    client.post("/workouts", json={"name": "Push Day"})
    res = client.get("/workouts/1")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Push Day"


def test_get_workout_not_found(client):
    res = client.get("/workouts/999")
    assert res.status_code == 404


def test_get_all_workouts(client):
    client.post("/workouts", json={"name": "Workout A"})
    client.post("/workouts", json={"name": "Workout B"})
    res = client.get("/workouts")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_delete_workout(client):
    client.post("/workouts", json={"name": "To Delete"})
    res = client.delete("/workouts/1")
    assert res.status_code == 200
    assert client.get("/workouts/1").status_code == 404


def test_delete_workout_not_found(client):
    res = client.delete("/workouts/999")
    assert res.status_code == 404


# --- Exercise Tests ---

def test_get_exercises_empty(client):
    res = client.get("/exercises")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_exercise(client):
    res = client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Squat"
    assert data["muscle_group"] == "Legs"


def test_create_exercise_missing_name(client):
    res = client.post("/exercises", json={"muscle_group": "Legs"})
    assert res.status_code == 422


def test_create_exercise_missing_muscle_group(client):
    res = client.post("/exercises", json={"name": "Squat"})
    assert res.status_code == 422


def test_create_exercise_duplicate_name(client):
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    res = client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    assert res.status_code in (422, 500)


def test_get_exercise_by_id(client):
    client.post("/exercises", json={"name": "Deadlift", "muscle_group": "Back"})
    res = client.get("/exercises/1")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Deadlift"


def test_get_exercise_not_found(client):
    res = client.get("/exercises/999")
    assert res.status_code == 404


def test_get_all_exercises(client):
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    client.post("/exercises", json={"name": "Bench Press", "muscle_group": "Chest"})
    res = client.get("/exercises")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_delete_exercise(client):
    client.post("/exercises", json={"name": "Plank", "muscle_group": "Core"})
    res = client.delete("/exercises/1")
    assert res.status_code == 200
    assert client.get("/exercises/1").status_code == 404


def test_delete_exercise_not_found(client):
    res = client.delete("/exercises/999")
    assert res.status_code == 404


# --- WorkoutExercise Tests ---

def test_add_exercise_to_workout(client):
    client.post("/workouts", json={"name": "Full Body"})
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "sets": 3, "reps": 10})
    assert res.status_code == 201
    data = res.get_json()
    assert data["sets"] == 3
    assert data["reps"] == 10


def test_add_exercise_with_duration(client):
    client.post("/workouts", json={"name": "Cardio"})
    client.post("/exercises", json={"name": "Plank", "muscle_group": "Core"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "duration": 60.0})
    assert res.status_code == 201
    assert res.get_json()["duration"] == 60.0


def test_add_exercise_invalid_sets(client):
    client.post("/workouts", json={"name": "Full Body"})
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "sets": -1})
    assert res.status_code == 422


def test_add_exercise_invalid_reps(client):
    client.post("/workouts", json={"name": "Full Body"})
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "reps": 0})
    assert res.status_code == 422


def test_add_exercise_invalid_duration(client):
    client.post("/workouts", json={"name": "Cardio"})
    client.post("/exercises", json={"name": "Plank", "muscle_group": "Core"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "duration": -10.0})
    assert res.status_code == 422


def test_add_exercise_workout_not_found(client):
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    res = client.post("/workout_exercises", json={"workout_id": 999, "exercise_id": 1, "sets": 3})
    assert res.status_code == 404


def test_add_exercise_exercise_not_found(client):
    client.post("/workouts", json={"name": "Full Body"})
    res = client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 999, "sets": 3})
    assert res.status_code == 404


def test_workout_includes_exercises(client):
    client.post("/workouts", json={"name": "Full Body"})
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "sets": 4, "reps": 8})
    res = client.get("/workouts/1")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["workout_exercises"]) == 1
    assert data["workout_exercises"][0]["exercise"]["name"] == "Squat"


def test_delete_workout_cascades(client):
    client.post("/workouts", json={"name": "Full Body"})
    client.post("/exercises", json={"name": "Squat", "muscle_group": "Legs"})
    client.post("/workout_exercises", json={"workout_id": 1, "exercise_id": 1, "sets": 3})
    client.delete("/workouts/1")
    with app.app_context():
        assert WorkoutExercise.query.count() == 0
