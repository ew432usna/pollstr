from flask import Flask, request, jsonify, redirect, render_template, url_for
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'polls.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = get_db_connection()
    # TODO: Complete schema definitions
    conn.execute('''CREATE TABLE IF NOT EXISTS poll (
                        id INTEGER PRIMARY KEY AUTOINCREMENT
                        
                    );''')
    conn.execute('''CREATE TABLE IF NOT EXISTS vote (
                        id INTEGER PRIMARY KEY AUTOINCREMENT
                    );''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # TODO: Retrieve a list of poll id, question, and current vote count, 
    # ordered by vote count descending (most popular first) 
    polls = [
        # [ID, Question, Total Votes (all choices)]
        [0,"What is the best ERC elective?",300],
        [1,"Who will win Army Navy in 2025?",78],
        [2,"What is Dr Donnal's best tie?", 35]
    ]
    return render_template('index.html', polls=polls)

@app.route('/poll/new', methods=['GET'])
def new_poll():
    # Nothing to do here :)
    return render_template('new_poll.html')

@app.route('/poll', methods=['POST'])
def create_poll():
    # TODO: create a new poll based on the user's submission:
    # submission has 4 fields: question, option1, option2, and option3
    # retrieve these values and create a new poll entry in the database
    
    
    # redirect back to the index page (/)
    return redirect('/')

@app.route('/poll/<int:id>', methods=['GET'])
def show_poll(id):
    # TODO: retrieve the specified poll given the id and show the votes for each option
    
    question = "What is Dr Donnal's best tie?"
    options = ["The Halloween one","The Princeton one","The one with black and orange"]
    votes = [10,20,5]
    return render_template('poll.html', question=question, options=options, votes=votes)

@app.route('/poll.json', methods=['GET'])
def get_random_poll():
    # TODO: return a random poll as JSON so the IoT device can display it
   
    return jsonify({'id':2,
                    'question':"What is Dr Donnal's best tie?",
                    'options':["The Halloween one",
                               "The Princeton one",
                               "The one with black and orange"]})

@app.route('/poll/<int:id>.json', methods=['POST'])
def vote_poll(id):
    # TODO: record a vote for a particular poll and save to the database

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=3000)
