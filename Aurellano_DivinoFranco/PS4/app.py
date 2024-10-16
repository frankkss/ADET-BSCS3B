from flask import Flask, render_template, request, jsonify
import json
import json
import os
# import mariadb
import sys


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('signIn.html')

@app.route('/signUp', methods=['POST'])
def submit():
    info = request.form.to_dict()
    

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="localhost",
            port=3306,
            database="PS"

        )
        # Get Cursor
        cur = conn.cursor()
        # cur.execute
        sequel_query = f'INSERT INTO USER VALUES("{info['f_name']}","{info['m_name']}", "{info['l_name']}", "{info['c_number']}", "{info['email']}", "{info['address']}");'
        # return sequel_query
        cur.execute(sequel_query)
    except mariadb.Error as e:
        return f"Error connecting to MariaDB Platform: {e}"

    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/users')
def users():
    try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="localhost",
            port=3306,
            database="PS"

        )
    except mariadb.Error as e:
        return f"Error connecting to MariaDB Platform: {e}"

    cur = conn.cursor()

    cur.execute("SELECT * FROM User")
    dbData =[]
    for a in cur:
        dbData.append(a)
    return dbData

if __name__ == "__main__":
    app.run(debug=True)