from datetime import date, timedelta
from flask import Flask
from .config import DevConfig
from flask_wtf.csrf import CSRFProtect
from .schema import HabitForm, HabitCompletedForm

csrf = CSRFProtect()

def create_app(env_config=DevConfig):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    csrf.init_app(app)
    app.config.from_object(env_config)

    from .db import InitDb
    app.db = InitDb(app).get_db()
    app.habit_form = HabitForm
    app.habit_completed_form = HabitCompletedForm

    from .routes import index, completed_habits
    app.register_blueprint(index.bp)
    app.register_blueprint(completed_habits.bp)

    @app.template_filter('get_date')
    def get_date(original_date: date, num:int):
        date_difference = timedelta(num)
        new_date = original_date + date_difference
        return new_date

    return app