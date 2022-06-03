from flask import Blueprint, redirect, render_template, current_app, url_for
from datetime import datetime
from pymongo.collection import Collection
import math

bp = Blueprint("index", __name__)

today_date_str = datetime.now().strftime("%Y-%m-%d")


@bp.route("/")
@bp.route("/habits/<calendar_day>/", methods=("POST", "GET"))
@bp.route("/habits/<calendar_day>/<int:page>/", methods=("POST", "GET"))
def habit_tracker(calendar_day: str = today_date_str, page: int = 1) -> None:
    """The habit tracker day that shows all habits for a particular day, day defaults to present day if no date is given"""

    habit_form = current_app.habit_form()
    habit_completed_form = current_app.habit_completed_form()
    habits: Collection = current_app.db.habits

    if habit_form.validate_on_submit():
        habit_data = {"habit": habit_form.habit.data, "date_started": habit_form.date_started.data}
        habits.insert_one(habit_data)
        return redirect(url_for("index.habit_tracker", calendar_day=calendar_day)), 302

    cal_date = datetime.strptime(calendar_day, "%Y-%m-%d")
    filter = {"date_started": {"$lte": cal_date}}
    page_to_skip = (page - 1) * 5
    day_habits_count = habits.count_documents(filter=filter)
    no_of_pages = math.ceil(day_habits_count / 5)
    pipeline = [
        {"$match": filter},
        {"$sort": {"_id": -1}},
        {"$skip": abs(page_to_skip)},
        {"$limit": 5},
        {
            "$lookup": {
                "from": "completedhabits",
                "localField": "_id",
                "foreignField": "habit",
                "pipeline": [
                    {
                        "$match": {"date_completed": cal_date}
                    }
                ],
                "as": "completed_habits",
            }
        },
        {
            "$addFields": {
                "completed": {
                    "$cond": [
                        {
                            "$eq": [
                                {
                                    "$first": "$completed_habits.date_completed"
                                },cal_date
                            ]
                        },
                        1,
                        0
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 1,
                "habit": 1,
                "completed": 1,
            }
        }
    ]
    day_habits = habits.aggregate(pipeline)

    return render_template(
        "index.html",
        date=cal_date,
        habit_form=habit_form,
        habit_completed_form=habit_completed_form,
        day_habits=day_habits,
        total_habits=day_habits_count,
        page=page,
        no_of_pages=no_of_pages,
    )
