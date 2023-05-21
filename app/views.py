from werkzeug.utils import redirect
from app import app, db
from app.models import User
from flask import json, render_template, request, session, url_for, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash

import os
import make_response
from flask_wtf.csrf import CSRFProtect


import nltk

nltk.download("popular")
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import sqlite3
from flask import g
from datetime import datetime
import datetime
import pytz
from keras.models import load_model
import uuid
from app import app, db

model = load_model("model.h5")
import json
import random

intents = json.loads(open("app/data.json").read())
words = pickle.load(open("texts.pkl", "rb"))
classes = pickle.load(open("labels.pkl", "rb"))
# DATABASE = 'chat_history.db'

csrf = CSRFProtect(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/register-user", methods=["POST"])
def register_user():

    if request.method == "POST":
        print("hiiiiiiiiiiiiii")
        print(request.form)

    form = request.form
    error_message_name = ""
    error_message_email = ""
    error_message_username = ""
    error_message_phone_number = ""
    error_message_password = ""

    flag = 0
    error_msg = []
    if (
        form["name"] != ""
        and form["username"] != ""
        and form["email-address"] != ""
        and form["phone-number"] != ""
        and form["password"] != ""
    ):
        print(form["username"])
        print(form["email-address"])

        username = User.query.filter_by(username=form["username"]).first()
        userEmail = User.query.filter_by(email=form["email-address"]).first()
        userPhoneNumber = User.query.filter_by(
            phone_number=form["phone-number"]
        ).first()
        print(username)
        print(userEmail)
        if username == None and userEmail == None and userPhoneNumber == None:
            print("create")
            user = User(
                name=form["name"],
                username=form["username"],
                email=form["email-address"],
                phone_number=form["phone-number"],
            )

            user.set_password(form["password"])
            db.session.add(user)
            db.session.commit()
            flag = 1
            error_msg.append("created")
            resp = {"flag": flag, "error_msg": error_msg}
        else:
            if username != None:
                print("ggggg")
                error_msg.append("User Already exits")
                # return render_template('signup.html', form=form,error_message  =  error_message)

            if userEmail != None:

                print("nnnnn")
                error_msg.append("Email Already exits")
                # return render_template('signup.html', form=form,error_message  =  error_message)

            if userPhoneNumber != None:

                print("cc")
                error_msg.append("Phone Already exits")
            resp = {"flag": flag, "error_msg": error_msg}

    else:
        if form["name"] == "":
            error_msg.append("Name cannot be empty")
        if form["email-address"] == "":
            error_msg.append("Email cannot be empty")
        if form["phone-number"] == "":
            error_msg.append("Phone Number cannot be empty")
        if form["password"] == "":
            error_msg.append("Password cannot be empty")
        if form["username"] == "":
            error_msg.append("Username cannot be empty")

        resp = {"flag": flag, "error_msg": error_msg}

    return jsonify(resp)


@app.route("/login_user", methods=["POST"])
def login_user():
    form = request.form
    user = User.query.filter_by(username=form["username"]).first()
    password = form["password"]
    # print(user.password_hash)
    print("hiiii" + generate_password_hash(password))

    if not user or not check_password_hash(user.password_hash, password):
        print("wrong")
        flash("Password was incorrect or user doesn't exist.")
        return render_template("index.html")
    else:

        session["username"] = form["username"]
        return redirect("/dashboard")
    # return redirect(url_for('auth.login'))


@app.route("/dashboard")
def dashboard():
    print("gggggg")
    if not session.get("username"):
        print("hiiii noooooooo")
        return render_template("index.html")
    else:
        print("hiiii vv")
        return render_template("dashboard.html")


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    return redirect(url_for("index"))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    return chatbot_response(userText)
