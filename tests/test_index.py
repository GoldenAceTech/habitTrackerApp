from datetime import datetime, timedelta
from typing import Callable
from flask import Flask, g, url_for
from flask.ctx import _AppCtxGlobals
from flask.testing import FlaskClient
import pytest
from random import randint, choice
from random_words import verbs
from pymongo.collection import Collection
from bson import ObjectId


random_date = datetime(randint(2022, 2023), randint(1, 12), randint(1, 28))


@pytest.fixture
def habits_db(app: Flask) -> list:
    """Gets the habit list for a particular day

    Args:
        app (Flask): _description_

    Returns:
        list: _description_
    """

    def _get_habits(day: datetime, limit: int, sort: int = -1) -> list[tuple]:
        habits = [habit for habit in app.db.habits.find({"date_started": {"$lte": day}}).sort("_id", sort).limit(limit)]
        return habits

    return _get_habits


def test_index(client: FlaskClient, app: Flask, habits_db: Callable):
    """Test for the index page"""
    response = client.get("/")
    today_date = datetime.now()
    today_str = today_date.strftime("%a")
    today_month_str = today_date.strftime("%b")
    today_date_str = today_date.strftime("%d")
    prev_three_day = (today_date + timedelta(days=-3)).day
    next_three_day = (today_date + timedelta(days=3)).day

    habits = habits_db(today_date, 5)

    # test to make sure the index page redirects to the habit tracker page and uses the current day date as the default day
    assert response.status_code == 200
    assert bytes(today_str, encoding="UTF-8") in response.data
    assert bytes(today_date_str, encoding="UTF-8") in response.data
    assert bytes(today_month_str, encoding="UTF-8") in response.data
    assert bytes(str(prev_three_day), encoding="UTF-8") in response.data
    assert bytes(str(next_three_day), encoding="UTF-8") in response.data
    print(dir(response.headers))

    # test that the current day habits are shown in descending order
    for habit in habits:
        assert bytes(habit["habit"], encoding="UTF-8") in response.data


def test_calendar_day(client: FlaskClient, habits_db: Callable):
    """Test for a calenday day"""
    response = client.get("/habits/2022-5-28/")

    habits = habits_db(datetime(2022, 5, 28), 5)
    # test to make sure the date generates the previous 3 days and the next three days
    assert b"May" in response.data
    assert b"Sat" in response.data
    assert b"28" in response.data
    assert b"2022-05-25" in response.data
    assert b"2022-05-31" in response.data

    # test to ensure the habits for the day are shown
    for habit in habits:
        assert bytes(habit["habit"], encoding="UTF-8") in response.data


def test_post(client: FlaskClient, app: Flask, habits_db: Callable):
    """Testing the post route"""
    client.get("/")
    habit_day = random_date
    csrf_token = g.get("csrf_token")
    habit = f"I will {choice(verbs)} and {choice(verbs)}"
    habit_data = {"csrf_token": csrf_token, "habit": habit, "date_started": habit_day}
    prev_doc_count = app.db.habits.estimated_document_count()
    date_str = habit_day.strftime("%Y-%m-%d")

    response = client.post(url_for("index.habit_tracker", calendar_day=date_str), data=habit_data)
    redirect_response = client.get(response.location)

    assert response.status_code == 302
    assert response.request.path == url_for("index.habit_tracker", calendar_day=date_str)
    assert app.db.habits.estimated_document_count() == prev_doc_count + 1

    # test new date posted is shown in
    habits = habits_db(habit_day, 5)
    assert bytes(date_str, encoding="UTF-8") in redirect_response.data
    assert bytes(habit, encoding="UTF-8") in redirect_response.data
    assert habits[0]["date_started"].strftime("%Y-%m-%d") == date_str


def test_form_error(client: FlaskClient, app: Flask, global_var: _AppCtxGlobals):
    """Testing the form error if user tries to post an invalid form"""
    habit_data = {"habit": "Play football today", "date_started": datetime(2022, 5, 28)}
    csrf_token = global_var.get("csrf_token")

    date_str = datetime(2022, 5, 28).strftime("%Y-%m-%d")
    url = url_for("index.habit_tracker", calendar_day=date_str)
    # requesting post without no csrf token
    response_nocsrf = client.post(url, data=habit_data)

    habit_data["habit"] = "ho"
    habit_data["csrf_token"] = csrf_token
    response_nohabit = client.post(url, data=habit_data)

    assert response_nocsrf.status_code == 400
    assert b"Habit must contain three(3) or more characters" in response_nohabit.data


def test_completed_habit(client: FlaskClient, app: Flask, habits_db: Callable, global_var: _AppCtxGlobals):
    """Testing the completed habit"""
    habits = habits_db(random_date, 1)
    habit_id = str(habits[0]["_id"])
    date_completed = random_date
    csrf_token = global_var.get("csrf_token")
    habit_completed_coll: Collection = app.db.completedhabits
    prev_doc_count = habit_completed_coll.estimated_document_count()

    completed_habit = {"habit": habit_id, "date_completed": date_completed, "csrf_token": csrf_token}

    post_url = url_for("completed_habits.completed_habit", id=habit_id)
    get_url = url_for("index.habit_tracker", calendar_day=random_date.strftime("%Y-%m-%d"))

    get_response = client.get(get_url)
    post_response = client.post(post_url, data=completed_habit)

    assert bytes(post_url, encoding="UTF-8") in get_response.data
    assert post_response.status_code == 302
    assert habit_completed_coll.estimated_document_count() == prev_doc_count + 1

    #test to check that a completed habit is marked uncompleted if it was previously completed 
    post_response_delete = client.post(post_url, data=completed_habit)

    assert habit_completed_coll.estimated_document_count() == prev_doc_count


def test_completed_habit_errors(client: FlaskClient, app: Flask, habits_db: Callable, global_var: _AppCtxGlobals):
    """Testing the completed habit post error"""
    habit_id = '0123456789abcdef257ecf6a'
    date_completed = random_date
    csrf_token = global_var.get("csrf_token")
    habit_completed_coll: Collection = app.db.completedhabits
    prev_doc_count = habit_completed_coll.estimated_document_count()

    completed_habit = {"habit": habit_id, "date_completed": date_completed, "csrf_token": csrf_token}
    completed_habit_invalid_form = {"habit": habit_id, "csrf_token": csrf_token}

    post_url = url_for("completed_habits.completed_habit", id=habit_id)
    get_url = url_for("index.habit_tracker", calendar_day=random_date.strftime("%Y-%m-%d"))

    get_response = client.get(get_url)
    post_response = client.post(post_url, data=completed_habit)
    #test for invalid form
    invalid_post_response = client.post(post_url, data=completed_habit_invalid_form)

    assert bytes(post_url, encoding="UTF-8") not in get_response.data
    assert post_response.status_code == 302
    assert invalid_post_response.status_code == 302
    assert habit_completed_coll.estimated_document_count() == prev_doc_count
