# Workout Tracker API

A RESTful backend API for a workout tracking application used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow.

---

## Description

Allows personal trainers to create and manage workouts, create reusable exercises, and associate exercises with workouts including sets, reps, or duration.

---

## Installation

```bash
git clone https://github.com/Brightvilla/Flask-SQLAlchemy-Workout-Backend.git
cd Flask-SQLAlchemy-Workout-Backend
pipenv install
pipenv shell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

---

## Run

```bash
flask run
```

API available at `http://127.0.0.1:5000`

---

## Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Get all workouts |
| GET | `/workouts/<id>` | Get a single workout with its exercises |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout |

**POST `/workouts` body:**
```json
{ "name": "Leg Day", "description": "Lower body focus" }
```

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | Get all exercises |
| GET | `/exercises/<id>` | Get a single exercise |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

**POST `/exercises` body:**
```json
{ "name": "Squat", "muscle_group": "Legs" }
```

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workout_exercises` | Add an exercise to a workout |

**POST `/workout_exercises` body:**
```json
{ "workout_id": 1, "exercise_id": 2, "sets": 3, "reps": 10 }
```
> Use `duration` (float, seconds) instead of `sets`/`reps` for timed exercises.

---

## Validations

**Table Constraints**
- `workouts.name` — NOT NULL
- `exercises.name` — NOT NULL, UNIQUE
- `workout_exercises.workout_id` / `exercise_id` — NOT NULL, foreign keys

**Model Validations**
- Workout/Exercise `name` must not be blank
- `sets`, `reps`, `duration` on WorkoutExercise must be positive numbers

**Schema Validations**
- `name` and `muscle_group` are required on POST
- `sets` and `reps` must be integers > 0
- `duration` must be a float > 0

---

## Dependencies

```
Flask==2.2.2
Flask-Migrate==3.1.0
Flask-SQLAlchemy==3.0.3
Werkzeug==2.2.2
marshmallow==4.3.0
SQLAlchemy==2.0.49
alembic==1.18.4
```

> Full list available in `requirements.txt`. Install with `pip install -r requirements.txt`.
