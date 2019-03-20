from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_formdata.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

#### Model definitions

class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    number_owned = db.Column(db.Integer)





#### Routes

@app.route('/')
def hello_world():
    return 'This is the main page. <a href="http://localhost:5000/form1">Click here to see the form.</a> <br><br> <a href="http://localhost:5000/all_vehicles">Click here to see all vehicles</a>.'

@app.route('/form1')
def form1():
    return render_template('form1.html')

@app.route('/result',methods=["GET"])
def result_form1():
    if request.method == "GET":
        print(request.args) # Check out your Terminal window where you're running this... to see
        if len(request.args) > 0:
            for k in request.args:
                poss_type = request.args.get(k,"None") # in two steps for clarity
                veh = Vehicle.query.filter_by(type=poss_type).first()
                if not veh:
                    veh = Vehicle(type=request.args.get(k,"None"),number_owned=0) # start
                    session.add(veh)
                    session.commit()
                veh.number_owned += 1
                session.add(veh)
                session.commit()
            return "Vehicles (or lack thereof) successfully noted. <br><br> <a href='http://localhost:5000/'>Go to the main page</a>"

@app.route('/all_vehicles')
def see_vehicles():
    vehs = Vehicle.query.all()
    return render_template('vehicles.html', vehicles=vehs)

@app.route('/form2')
def form2():
    return """<form action="http://localhost:5000/letter" method='GET'>
    <input type="text" name="phrase"><br>
    <input type="submit" value="Submit">
    """

@app.route('/letter',methods=["GET"])
def letters_result():
    if request.method == "GET":
        phrase = request.args.get('phrase','')
        total_number = 0
        for ch in phrase:
            if ch == "e":
                total_number += 1
        return "There were {} occurrence(s) of the letter e in the entered phrase".format(total_number)

    return "Nothing was submitted yet... <a href='http://localhost:5000/form2'>Go submit something</a>"


if __name__ == "__main__":
    db.create_all()
    app.run()
