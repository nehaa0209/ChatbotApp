RESTAURANT SUGGESTER ChatBot

DESCRIPTION:
We have created a website that has a chatbot which would help you to find new that would help everyone to find different 
type of restaurants according to their preferences. This system give you different kinds of food choices, the you can also 
name a suburb and ask the bot to find you a nice restaurant near that suburb. We created our own dataset to be used for the
chatbot responses. The chatbot was trained on this dataset. We used an Artificial neural network for training by classifying 
different the type of message sent by the user and giving up the responses accordingly. We even created a login and sign up page 
that has some constraints for client side validation we also used ajax for the server side validation. We had some problems with the history but were able 
to save it and print it in a simple form.

Dependencies:
For importing the libraries from python these installations are done. 
pip install tensorflow : This is a very useful library for data modeling
pip install keras : This is mainly to tokanize the data used in the data set
pip install pickle 
pip install nltk
pip install flask : This is mainl used to import and load data.

Steps to execute the code:
Login and Signup page:
We have created a login page as index.html. Firstly a user must signup and create an account then they should be able to login with correct id and password.
Chatbot creation:
The first step is to create, load and iport the data.json file. This file contains the user questions and chatbot reponses. This data 
is used for the actual working of the chatbot.
The second step is to create the training.py file. This file is a python file which is used to train the data according to the .json provided.
Next we will create the html and style.css files which is used to create the webpages.
Lastly for the chatbot we will have to display the app.py file which has the code for the chatbot functionality.'
There is a history button in the history button by clicking on it it takes yu to the chat_history page.




