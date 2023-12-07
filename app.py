from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://rockotest:rockotest1@rockotest.1hzo4qs.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
app = Flask(__name__)

# client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos

default_date = datetime.now(timezone.utc)
todos.update_many({'date_added': {'$exists': False}}, {'$set': {'date_added': default_date}})

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['priority']
        date_added = datetime.now(timezone.utc)
        todos.insert_one({'content': content, 'priority': degree, 'complete': False, 'date_added': date_added})
        return redirect(url_for('index'))

    all_todos = todos.find().collation({'locale': 'en'}).sort('content') 
    return render_template('index.html', todos=all_todos)

@app.route('/<id>/complete/', methods=['POST'])
def complete_todo(id):
    todos.update_one({'_id': ObjectId(id)}, {'$set': {'complete': True}})
    return redirect(url_for('index'))

@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))