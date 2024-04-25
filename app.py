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
    conn.execute('''CREATE TABLE IF NOT EXISTS "Poll" (
        "PollID" INTEGER NOT NULL UNIQUE,
        "Question" VARCHAR(255),
        "AnswerA" VARCHAR(100),
        "AnswerB" VARCHAR(100),
        "AnswerC" VARCHAR(100),
        "VoteA" INTEGER DEFAULT 0,
        "VoteB" INTEGER DEFAULT 0,
        "VoteC" INTEGER DEFAULT 0,
        "TotalVotes" INTEGER DEFAULT 0,
        PRIMARY KEY("PollID" AUTOINCREMENT)
        );''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    # TODO: Retrieve a list of poll id, question, and current vote count, 
    # ordered by vote count descending (most popular first) 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT PollID, Question, TotalVotes FROM Poll ORDER BY TotalVotes DESC;''')
    polls = cur.fetchall() 
    cur.close()
    conn.close()
    print(polls)
    return render_template('index.html', polls=polls)

@app.route('/poll/new', methods=['GET'])
def new_poll():
    # Nothing to do here :)
    return render_template('new_poll.html')

@app.route('/poll', methods=['POST'])
def create_poll():
    # Retrieve values from the user's submission
    question = request.form['Question']
    option1 = request.form['AnswerA']
    option2 = request.form['AnswerB']
    option3 = request.form['AnswerC']
    
    # Create a new poll entry in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Poll (Question, AnswerA, AnswerB, AnswerC) 
                      VALUES (?, ?, ?, ?)''', (question, option1, option2, option3))
    conn.commit()
    conn.close()
    
    # Redirect back to the index page
    return redirect('/')


@app.route('/poll/<int:id>', methods=['GET'])
def show_poll(id):
    # TODO: retrieve the specified poll given the id and show the votes for each option
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT Question,AnswerA,AnswerB,AnswerC,VoteA,VoteB,VoteC FROM Poll WHERE PollID = ?",[id])
    pollinfo = c.fetchall()
    print(pollinfo)
    print(pollinfo[0][0])
    conn.close()
    
    question = pollinfo[0][0]
    options = [pollinfo[0][1],pollinfo[0][2],pollinfo[0][3]]
    votes = [pollinfo[0][4],pollinfo[0][5],pollinfo[0][6]]
    return render_template('poll.html', question=question, options=options, votes=votes)

@app.route('/poll.json', methods=['GET'])
def get_random_poll():
    # TODO: return a random poll as JSON so the IoT device can display it
    conn = get_db_connection()
    c = conn.cursor()
    # get all the polls
    c.execute("SELECT PollID,Question,AnswerA,AnswerB,AnswerC FROM Poll")
    # pick a random one
    poll = random.choice(c.fetchall())
    # unpack the list into the JSON structure the embedded device expects
    return jsonify({'id':poll[0],
                    'question':poll[1],
                    'options':poll[2:]})

@app.route('/poll/<int:id>.json', methods=['POST'])
def vote_poll(id):
    selected_option = request.json['option'] # A B or C
    # sanitize the selected option to avoid SQL Injection
    if selected_option == 'A':
        option = 'VoteA'
    elif selected_option =='B':
        option = 'VoteB'
    elif selected_option =='C':
        option='VoteC'
    else:
        option='VoteA' # default if a hacker puts something unexpected in
    print(f"Recording a new vote for {option} on question {id}")

    conn =  get_db_connection()
    c = conn.cursor()
    # retrieve the current vote count
    c.execute(f"SELECT {option},TotalVotes FROM Poll WHERE PollID=?",(id,))
    vote_count,total_votes = c.fetchone()
    # increment it
    vote_count += 1
    total_votes += 1
    # save the vote count back to the database
    c.execute(f"UPDATE Poll SET {option}=?,TotalVotes=? WHERE PollID=?",(vote_count,total_votes,id))
    conn.commit()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=3000)
