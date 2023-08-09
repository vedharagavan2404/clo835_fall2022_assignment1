from flask import Flask, render_template, request, current_app
from pymysql import connections
import os
import random
import argparse
import requests

app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "white"
DBPORT = int(os.environ.get("DBPORT", 3306))
BACKGROUND_IMAGE_URL = os.environ.get("BACKGROUND_IMAGE_URL") or "https://assignmentsree.s3.us-east-1.amazonaws.com/download.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIHiHSjK2%2B0NLsMUzm%2BjjRcytzFnfuN5AExw7df4WSjBDAiEA%2BkRC09LpIYkXn3Zs0rTnvkld2IZYaTuW6n3b%2BSUwRP8q%2FQIIm%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw3MDg1MTk1NzEzNDciDI7T5J1GTV5gJkBG4CrRAthgvicOLvfWTCBL4tQyt5s8kj678ptRv6NljJbSHn5YcVQ5H2sh49U9rpcXpcgzoHyqOnY%2BNQYvrgveYI4t3TgeqogRm6MGngBWNvW47D%2B9uZI70mssilYvUcQm1FWaAZEBTxoWsB6RGq7cdERGJ1QGNVwXvLWrrg%2BlF38pqMaNHcXdsG%2FH2RSvhRlDDhEfGkzqjwtcxTbLOdvTr5h0IEH2m5KgMmbNC%2FGK7c%2BzqRhh1PcmJWeXdWKVrcA8jBOeV7u73JkL4lHJBzvuyJBzwPBDcmGDleTaBwsEpYzQU8M6Z8jEqWDmhlCU2OBKwtfAwcjzkSDFt9K0o8Dyhnnt6OwM3PA9nfGE5I2jyLS3gfDkRX5B%2B6AxSYfhhwHNwiKRthK4zBH9KEPYisURy2KhfmZco%2BfdNgqlg4PT%2FibaccvCbMyZt%2BpvN3z7XlMZrgZ5Dzwwh%2B7LpgY6hwI2NMJU93RXWAYMyURyjX47vruntQT5%2FAMIHJhh2sL%2BxS52SxDymZJfDuzjhkPSuYpBH1uHq%2BmuqVu1MaBkcu9l2CoVFzUz70crgGCDbeY0ombmVXc2Kg%2BXzBXUC3x9s6mo9RAGSuBOeoHdkEcFvJV8TAsfQhQLF%2BtaLsp54vEaCzFdY0JnuvLksvUPbcYTqZy0j0TkKdMy3pOlG5jR3t5yscut37QqobcRVuRGNIxxVTbwxPZ4WtuFCOFNN9JcuMdyWNKtrpcFLpysw4gj%2B5wqq%2BpChYvMJHg%2F0hOGnMnLbOAvNPpg15SXoVNpI9BABS%2FCICzg5jFyJVScuJGlqhh7u%2BpbzvW23Q%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230809T022403Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA2J5YOV6JY6ULBJ7M%2F20230809%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=3d6471a8e6c929cc7d1ef7cdaf510dee95068a56f6e6437434b397138ec2e34f"
YOUR_NAME = os.environ.get("YOUR_NAME", "SENECA_TEAM")  or "Sree"

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}


# Create a string of supported colors
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
COLOR = COLOR_FROM_ENV


@app.route("/", methods=['GET', 'POST'])
def home():
    app.logger.info(f"Background image URL: {BACKGROUND_IMAGE_URL}")
    return render_template('addemp.html', background_image=BACKGROUND_IMAGE_URL, your_name=YOUR_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    app.logger.info(f"Background image URL: {BACKGROUND_IMAGE_URL}")
    return render_template('about.html', background_image=BACKGROUND_IMAGE_URL, your_name=YOUR_NAME)
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR])

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR])


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], color=color_codes[COLOR])

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()
    your_name = os.environ.get("YOUR_NAME", "SENECA_TEAM")
    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)
