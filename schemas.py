from marshmallow import Schema, fields, validates, ValidationError, validate


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(load_default=None)
    reps = fields.Int(load_default=None)
    duration = fields.Float(load_default=None)
    exercise = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "muscle_group")), dump_only=True)

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive integer.")

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer.")

    @validates("duration")
    def validate_duration(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be a positive number.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name must not be empty."))
    description = fields.Str(load_default=None)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Name must not be empty."))
    muscle_group = fields.Str(required=True, validate=validate.Length(min=1, error="Muscle group must not be empty."))
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema(exclude=("exercise",))), dump_only=True)


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
