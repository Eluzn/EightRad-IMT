# app.py (Flask application)
from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = 'messages.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    message = request.form.get('message')
    nickname = request.form.get('nickname') # Get nickname from POST request
    if message and nickname: # check nickname exists
        conn = get_db_connection()
        timestamp = datetime.datetime.now().isoformat()  # Get current timestamp
        conn.execute('INSERT INTO messages (message, nickname, timestamp) VALUES (?, ?, ?)', (message, nickname, timestamp))  # Store timestamp
        conn.commit()
        conn.close()
    return jsonify({'success': True})

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    # (In a real app, verify moderator privileges here)
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/messages') # new route to get messages
def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 100').fetchall() # Get latest 100 messages
    conn.close()
    return jsonify([dict(msg) for msg in messages]) # jsonify needs a dictionary



if __name__ == '__main__':
    # Create the database if it doesn't exist
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            nickname TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    ''')
    conn.close()
    app.run(debug=False, host='0.0.0.0')