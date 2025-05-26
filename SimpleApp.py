# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect
import sqlite3
import psycopg2
import os
import webbrowser
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')


def init_db():
    conn = get_db_connection()
    c = conn.cursor()  # cursor
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses(
        first_name TEXT,
        last_name TEXT,
        attendes TEXT,
        members INTEGER,
        PRIMARY KEY (first_name, last_name))
    ''')
    conn.commit()
    conn.close()
@app.route('/',methods=['GET'])
def homePage():
    return render_template("example.html")


@app.route('/submit',methods=['POST'])
def submit():
    first_name=request.form['first_name']
    last_name = request.form['last_name']
    attendes = request.form.get('attendes')
    if attendes=="no":
        members=0
    else:
        members=request.form.get('members')
    conn = get_db_connection()
    c = conn.cursor()  # cursor
    try:
        c.execute('''
                    INSERT INTO responses (first_name, last_name, attendes, members)
                    VALUES (?, ?, ?, ?)
                ''', (first_name,last_name, attendes, members)
                  )
    except:
        c.execute('''
                    UPDATE responses
                    SET attendes = ?, members = ?
                    WHERE first_name = ? AND last_name = ?
                ''', (attendes, members, first_name, last_name))
    conn.commit()
    conn.close()
    return redirect('/')


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    init_db()
    app.run()