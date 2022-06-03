from flask import Blueprint, redirect, current_app, request, url_for
from datetime import datetime
from pymongo.collection import Collection
from bson.objectid import ObjectId

bp = Blueprint("completed_habits", __name__)


@bp.post("/habits/<string:id>/completed")
def completed_habit(id) -> None:
    """Save completed habit with date completed and redirect to habit tracker page

    Args:
        id (_type_): habit id
        date_completed (_type_): The date habit got completed
    """
    form = current_app.habit_completed_form()
    completed_habits_collection: Collection = current_app.db.completedhabits
    habits_collection: Collection = current_app.db.habits

    if form.validate_on_submit():
        date_completed = form.date_completed.data
        habit_completed = {"habit": ObjectId(form.habit.data), "date_completed": date_completed}

        if habits_collection.count_documents(filter={"_id": ObjectId(form.habit.data)}) >= 1:
            if completed_habits_collection.count_documents(filter=habit_completed):
                completed_habits_collection.delete_one(habit_completed)
            else:
                completed_habits_collection.insert_one(habit_completed)

    habit_day = form.date_completed.data or datetime.now()
    redirect_url = request.referrer or url_for("index.habit_tracker", calendar_day=habit_day.strftime("%Y-%m-%d"))
    return redirect(redirect_url)
