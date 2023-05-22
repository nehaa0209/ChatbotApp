
from werkzeug.utils import redirect
from app import app, db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from app.models import User,Chat
from flask import json, render_template, request, session, url_for, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import os
import make_response
from flask_wtf.csrf import CSRFProtect
import nltk
nltk.download('popular')
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

model = load_model('model.h5')
import json
import random
intents = json.loads(open('app/data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))


csrf = CSRFProtect(app)

# index page
@app.route('/')
def index():
    return render_template('index.html')
    
#signup page    
@app.route('/signup')
def signup():
    return render_template('signup.html')
    
# function to register the users with server side vallidations    
@app.route('/register-user', methods=['POST'])
def register_user():
    
    if request.method == "POST":
        form = request.form
        error_message_name = ''
        error_message_email = ''
        error_message_username = ''
        error_message_phone_number = ''
        error_message_password = ''
    
    flag = 0
    error_msg= []
    if form['name'] != '' and form['username'] != '' and form['email-address'] != '' and form['phone-number'] != '' and form['password'] != '':

        username = User.query.filter_by(username=form['username']).first()
        userEmail = User.query.filter_by(email=form['email-address']).first()
        userPhoneNumber = User.query.filter_by(phone_number=form['phone-number']).first()

        if username==None and userEmail ==None and userPhoneNumber == None:
            user = User(
                name=form['name'],
                username=form['username'],
                email=form['email-address'],
                phone_number=form['phone-number']
            )
        
            user.set_password(form['password'])
            db.session.add(user)
            db.session.commit()
            flag = 1
            error_msg.append("created")
            resp = {"flag" : flag, "error_msg" : error_msg}
        else:
            if username != None:
                error_msg.append("User Already exits")
               
            if userEmail != None:
                error_msg.append("Email Already exits")
            if userPhoneNumber != None:
                error_msg.append("Phone Already exits")
            resp = {"flag" : flag, "error_msg" : error_msg} 
                
    else:
        if form['name'] == '':
            error_msg.append("Name cannot be empty")
        if form['email-address'] == '':
            error_msg.append("Email cannot be empty")
        if form['phone-number'] == '':
            error_msg.append("Phone Number cannot be empty")
        if form['password'] == '':
            error_msg.append("Password cannot be empty")
        if form['username'] == '':
            error_msg.append("Username cannot be empty")                 
            
        resp = {"flag" : flag, "error_msg" : error_msg}       
            
    
    return jsonify(resp)
    
# Login functionality for user
@app.route('/login_user', methods=['POST'])
def login_user():
    form = request.form
    user = User.query.filter_by(username=form['username']).first()
    password = form['password']
   
    if not user or not check_password_hash(user.password_hash, password):
        return render_template('index.html', msg_login = "Password was incorrect or user doesn't exist.")
    else:
        session['username'] = form['username']
        return redirect('/dashboard')
       
       
# dashboard page with session check       
@app.route('/dashboard')
def dashboard():
    if not session.get("username"):
        return render_template("index.html")
    else:
        return render_template("dashboard.html")

        
#logout functionality        
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))    
    
#Saving the history    
@app.route("/history" , methods=['GET','POST'])
def history():
    if not session.get("username"):
        return render_template("index.html")
    else:
        form = request.form
        chat = Chat.query.filter_by(username=form['username']).all()
        for i in chat:
            #print(chat.user)
            print(i.username)
            print(i.user)
            print(i.bot)
    

        return render_template("history.html", chat_history=chat)
    
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
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

# Function to get bot response
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    username = request.args.get('username')
    response = chatbot_response(userText)
    save_chat_history(username, userText, response)
    return chatbot_response(userText)


# function to save the chat
def save_chat_history(usr, user_message, bot_response):
    print("in save history")  
    chat = Chat(
            username  =  usr,
            user=user_message,
            bot=bot_response
        )
    db.session.add(chat)
    db.session.commit()
    







    


