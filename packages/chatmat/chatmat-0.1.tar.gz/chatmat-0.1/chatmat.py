# chatmat.py

import sqlite3
import difflib

class Chatbot:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatbot_data (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer TEXT
            )
        ''')
        self.conn.commit()

    def train(self, question, answer):
        self.cursor.execute('INSERT INTO chatbot_data (question, answer) VALUES (?, ?)', (question, answer))
        self.conn.commit()

    def test(self, question):
        self.cursor.execute('SELECT question, answer FROM chatbot_data')
        data = self.cursor.fetchall()
        similar_questions = difflib.get_close_matches(question, [q[0] for q in data], n=1, cutoff=0.6)
        
        if similar_questions:
            best_match = similar_questions[0]
            index = [q[0] for q in data].index(best_match)
            return data[index][1]
        else:
            return "Sorry, I don't have an answer to that."

    def close(self):
        self.conn.close()