# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import psycopg2
import os

DB_HOST = "dpg-d0plevbuibrs73fuonc0-a.oregon-postgres.render.com"
DB_PORT = 5432
DB_NAME = "guestslist"
DB_USER = "guestslist_user"
DB_PASSWORD = "Njc2Lsxt9xL26DJxQl8w62OKRAuqmosk"

app = Flask(__name__)
def get_db_connection():
        # Connect to the database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return  conn


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
    return render_template("testPage.html")


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
    c.execute('''INSERT INTO responses (first_name, last_name, attendes, members)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (first_name, last_name)
        DO UPDATE SET
            attendes = EXCLUDED.attendes,
            members = EXCLUDED.members;
    ''', (first_name, last_name, attendes, members))
    conn.commit()
    conn.close()
    return redirect(url_for('thank_you'))
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')
@app.route('/responses',methods=['GET'])
def sqlQueries():
    conn = get_db_connection()
    c = conn.cursor()  # cursor
    c.execute("SELECT * FROM responses;")
    rows = c.fetchall()
    conn.close()
    return '<br>'.join([str(row) for row in rows])
# main driver function
if __name__ == '__main__':

    sqlQueries()