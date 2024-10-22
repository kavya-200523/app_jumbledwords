
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from random import randrange, choice
import os

# Set the template folder location
template_dir = os.path.abspath('C:/Users/kavya/OneDrive/Documents/templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "your_secret_key"

# Connect to the MySQL database for Jumbled Words and Morse Code games
def get_db_connection(db_name):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Laksh232005$",  # Replace with your MySQL password
        database=db_name
    )

# Route for the homepage (start page)
@app.route('/')
def index():
    # Reset the score when starting a new game
    session['score'] = 0
    return render_template('index.html')

# Route for game selection (choose between Jumbled Words or Morse Code)
@app.route('/select_game')
def select_game():
    # Reset the score when a new game starts
    session['score'] = 0
    return render_template('game_select.html')

# Jumbled Words Game
@app.route('/jumbled', methods=['GET', 'POST'])
def jumbled_game():
    message = ""
    correct = True

    # Always fetch the latest data from the database to ensure updates are reflected
    conn = get_db_connection('jumbled')
    cursor = conn.cursor()
    cursor.execute("SELECT incorrect, correct FROM k1")
    jumbled_words = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        # Check if the user clicked Exit
        if 'exit' in request.form:
            return redirect(url_for('index'))

        # Get the user's answer
        user_answer = request.form.get('answer', '').upper()
        correct_answer = jumbled_words[session['word_index']][1]

        if user_answer == correct_answer:
            session['score'] += 5  # Increase score by 5 for correct answers
            message = 'Correct Answer!'
            correct = True
        else:
            message = f'Incorrect! The correct answer was: {correct_answer}'
            correct = False

    # Pick a new random word for the next round
    word_index = randrange(len(jumbled_words))
    session['word_index'] = word_index
    jumbled_word = jumbled_words[word_index][0]

    return render_template('jumbled_game.html', jumbled_word=jumbled_word, score=session['score'], message=message, correct=correct, time_left=15)

# Morse Code Game
@app.route('/morse', methods=['GET', 'POST'])
def morse_game():
    message = ""
    correct = True

    # Always fetch the latest data from the database to ensure updates are reflected
    conn = get_db_connection('morse_code_game')
    cursor = conn.cursor()
    cursor.execute("SELECT char_value, morse_code FROM morse_code_dict")
    morse_code_data = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        # Check if the user clicked Exit
        if 'exit' in request.form:
            return redirect(url_for('index'))

        # Get the user's answer
        user_answer = request.form.get('answer', '').upper()
        correct_answer = morse_code_data[session['letter_index']][0]

        if user_answer == correct_answer:
            session['score'] += 5  # Increase score by 5 for correct answers
            message = 'Correct Answer!'
            correct = True
        else:
            message = f'Incorrect! The correct answer was: {correct_answer}'
            correct = False

    # Pick a new random Morse Code for the next round
    letter_index = choice(list(range(len(morse_code_data))))
    session['letter_index'] = letter_index
    morse_code = morse_code_data[letter_index][1]

    return render_template('morse_game.html', morse_code=morse_code, score=session['score'], message=message, correct=correct, time_left=15)

if __name__ == '__main__':
    app.run(debug=True)
