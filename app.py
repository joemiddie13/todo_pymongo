from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['priority']
        todos.insert_one({'content': content, 'priority': degree})
        return redirect(url_for('index'))

    all_todos = todos.find() # Add this line outside the if block! 
    return render_template('index.html', todos=all_todos) # add todos here! 