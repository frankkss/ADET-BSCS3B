from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import hashlib
import json
import os
# import mariadb
import sys
import hashlib


app = Flask(__name__)
app.secret_key = "my_secret_key"
@app.route('/')
def index():
    if 'userInfo' in session:
        data = session['userInfo']
        return redirect('/dashboard')
    else:
        data={
            "Username": "",
            "error": ""
        }
        return render_template('signIn.html', data=data)

@app.route('/signin', methods=['POST'])
def signIn():
    info = request.form.to_dict()   
    dbData = None 
    """
     try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="localhost",
            port=3306,
            database="REGISTERDB"

        )
        # Get Cursor
        cur = conn.cursor()
        # cur.execute
        sequel_query = f'SELECT TOP 1 * FROM USERS WHERE Username="{info['username']}"'        
        cur.execute(sequel_query)

        dbData = cur.fetchone()

        conn.close()

    except mariadb.Error as e:
        data = {
            error: "Error connecting to database. Please try again later."
        }

        return render_template('signIn.html', data=data)  
    
    """
    #mock data for testing

    dbData = {
        "Username": "frank",
        "f_name": "Divino",
        "m_name": "R",
        "l_name": "Aurellano",
        "c_number": "09123456789",
        "email": "abc@gmail.com",
        "address": "1234 abc st.",
        "Password": hashlib.sha256(("123").encode()).hexdigest()
    }   


    if dbData is None:
        errorData = {"Username":info["username"], "error": "Invalid Username or Password"}
        return render_template('signIn.html', data=errorData)
    elif dbData["Username"] == info["username"] and dbData["Password"] ==  hashlib.sha256(info["password"].encode()).hexdigest(): #add encryption to info["password"]
        data = {
            "Username": dbData["Username"],
            "f_name": dbData["f_name"],
            "m_name": dbData["m_name"],
            "l_name": dbData["l_name"],
            "c_number": dbData["c_number"],
            "email": dbData["email"],
            "address": dbData["address"]
        }   
        
        session['userInfo'] = data
        return redirect('/dashboard')
        #return render_template('dashboard.html', data=data)            
    else:
        errorData = {"Username":info["username"], "error": "Invalid Username or Password"}
        return render_template('signIn.html', data=errorData)


@app.route('/signup')
def signup():
    data={
        "Username": "",
        "error": ""
    }
    return render_template('signUp.html', data=data)


@app.route('/signup', methods=['POST'])
def submit():
    info = request.form.to_dict()
    
    dbData = None
    """
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="localhost",
            port=3306,
            database="REGISTERDB"

        )
        # Get Cursor
        cur = conn.cursor()

        encryptedPW = hashlib.sha256(info["password"].encode())  #add encrption here
        sequel_query = f'INSERT INTO USER VALUES("{info['Username']}","{encryptedPW}","{info['f_name']}","{info['m_name']}", "{info['l_name']}", "{info['c_number']}", "{info['email']}", "{info['address']}");'
        # return sequel_query
        cur.execute(sequel_query)
    except mariadb.Error as e:
        errorData = {"error": "Error connecting to database. Please try again later."}
        return render_template('signUp.html', data=errorData)
    
        
    conn.commit()
    conn.close() 

    """

    data = {
    "f_name": info['f_name'], 
    "m_name": info['m_name'], 
    "l_name": info['l_name'], 
    "c_number": info['c_number'], 
    "email":info['email'], 
    "address": info['address'], 
    "Username": info['username']
    }
    session['userInfo'] = data
    return redirect('/dashboard')

#test for dashboard page
@app.route('/dashboard')
def dash():
    """
    data = {
        "Username": "frank",
        "f_name": "Divino",
        "m_name": "R",
        "l_name": "Aurellano",
        "c_number": "09123456789",
        "email": "abc@gmail.com",
        "address": "1234 abc st.",
        "Password": "123"
    }   
    return render_template('dashboard.html', data=data)

"""
    if 'userInfo' in session:
        data = session['userInfo']
        return render_template('dashboard.html', data=data)
    else:
        data={
        "Username": "",
        "error": ""
        }
        return render_template('signIn.html', data=data)    

@app.route('/signout')
def signout():
    session.pop('userInfo', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)