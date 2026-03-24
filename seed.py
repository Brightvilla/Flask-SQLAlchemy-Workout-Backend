from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    db.drop_all()
    db.create_all()

    # Exercises
    squat = Exercise(name="Squat", muscle_group="Legs")
    bench = Exercise(name="Bench Press", muscle_group="Chest")
    deadlift = Exercise(name="Deadlift", muscle_group="Back")
    pullup = Exercise(name="Pull-Up", muscle_group="Back")
    plank = Exercise(name="Plank", muscle_group="Core")

    db.session.add_all([squat, bench, deadlift, pullup, plank])
    db.session.commit()

    # Workouts
    w1 = Workout(name="Full Body Strength", description="A complete strength training session.")
    w2 = Workout(name="Upper Body Blast", description="Focus on chest and back.")
    w3 = Workout(name="Core & Endurance", description="Core stability and endurance work.")

    db.session.add_all([w1, w2, w3])
    db.session.commit()

    # WorkoutExercises
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, sets=4, reps=10),
        WorkoutExercise(workout_id=w1.id, exercise_id=deadlift.id, sets=3, reps=8),
        WorkoutExercise(workout_id=w2.id, exercise_id=bench.id, sets=4, reps=12),
        WorkoutExercise(workout_id=w2.id, exercise_id=pullup.id, sets=3, reps=10),
        WorkoutExercise(workout_id=w3.id, exercise_id=plank.id, sets=3, duration=60.0),
    ])
    db.session.commit()

    print("Database seeded successfully!")
