import os, sqlite3

class EventDatabase():
    def __init__(self, event_database_name):
        self.event_database_name = event_database_name
        self.final_path = 'events/' + self.event_database_name
        event_database_path = os.getcwd() + '/' + self.final_path
        if os.path.exists(event_database_path):
            pass
        else:
            self.create_table()
        return

    # database setup
    def create_table(self):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS questions (name TEXT, followers INT, question TEXT)')
        conn.close()
        return

    def add_question_to_db(self, name, followers, question):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO questions (name, followers, question) VALUES (?, ?, ?)', (name, followers, question))
        conn.commit()
        conn.close()
        return

    def get_questions_from_db(self):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        questions = [item[0] for item in c.execute('SELECT question FROM questions').fetchall()] # Only getting the question here
        conn.close()
        return questions

    def get_most_influential_question(self):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        # Query to get the row with the max followers
        c.execute('SELECT * FROM questions ORDER BY followers DESC LIMIT 1')
        max_followers_entry = c.fetchone()
        conn.close()
        return max_followers_entry

    def is_db_empty(self):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        # Query to get the count of rows in the table
        c.execute('SELECT COUNT(*) FROM questions')
        number_of_rows = c.fetchone()[0]
        conn.close()
        return number_of_rows == 0

    def get_random_questions(self):
        conn = sqlite3.connect(self.final_path + '.sqlite')
        c = conn.cursor()
        random_questions = [item[0] for item in c.execute('SELECT question FROM questions ORDER BY RANDOM() LIMIT 2')]
        conn.close()
        return random_questions
