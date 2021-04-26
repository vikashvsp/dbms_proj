from flask import Flask, render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from base64 import main
app = Flask(__name__) 
engine = create_engine("postgresql://postgres:qwerty@localhost:5433/covid_project")
db = scoped_session(sessionmaker(bind=engine))
@app.route("/")
def index():
    cases = db.execute("select * from cases").fetchall()
    return render_template("index.html",cases=cases)

@app.route("/Services")
def Services():
    cases = db.execute("select * from cases").fetchall()
    return render_template("servies.html",cases=cases)

@app.route("/Services/Registration", methods=["POST"])
def register():
    ad=request.form.get("adhno")
    fname=request.form.get("firstname")
    lname=request.form.get("lastname")
    age=request.form.get("age")
    sname=request.form.get("s_name")
    cname=request.form.get("city")
    gndr=request.form.get("gender")
    adrs=request.form.get("address")
    pin=request.form.get("pncd")
    test=request.form.get("tested")
    crit=request.form.get("critical")
    db.execute("INSERT INTO person (aadhar_no, fname, lname, age, gender, address, city, state, pincode, tested, critical) VALUES (:aadhar_no, :fname, :lname, :age, :gender, :address, :city, :state, :pincode, :tested, :critical)",
        { "aadhar_no": ad, "fname": fname, "lname": lname, "age": age, "gender": gndr, "address": adrs, "city": cname, "state": sname, "pincode": pin, "tested": test, "critical": crit})
    db.commit()
    if (test == 'Y' and crit == 'Y') or (test == 'N' and crit == 'Y'):
        hospitals = db.execute("SELECT * FROM hospital WHERE district=:district",{"district": cname}).fetchall()
        return render_template("bookhospital.html",fname=fname,hospitals=hospitals)
    elif (test =='Y' and crit == 'N'):
        centers = db.execute("SELECT * FROM qcenters WHERE district=:district",{"district": cname}).fetchall()
        return render_template("qcentre.html",fname=fname,centers=centers) 
    else:
        return render_template("success.html",fname=fname,type="Registration",message="Thankyou for registering with us. For any furthur help do visit our website.")

@app.route("/Services/Registration/Successful", methods=["POST"])
def book():
    hid=request.form.get("h_id")
    ad=request.form.get("adhno")
    prob=request.form.get("prb")
    db.execute("INSERT INTO patient(hid, problem, aadhar_no) VALUES (:hid, :problem, :aadhar_no)",{ "hid": hid, "problem": prob, "aadhar_no": ad})
    db.commit()
    return render_template("success.html",type="Booking",message="You have successfullly booked your hospital. Kindly visit your hospital! Hoping for your speedy recovey!")
@app.route("/Admin")
def admin():
    return render_template("admin.html")
@app.route("/Admin/Success", methods=["POST"])
def adminsuccess():
    usrname=request.form.get("uname")
    paswd=request.form.get("psw")
    cases=db.execute("SELECT * FROM cases").fetchall()
    if usrname=="rupesh123" and paswd=="12345":
        return render_template("modify.html",cases=cases)
    else:
        return render_template("error.html",message="Please enter valid user credentials and try again :(")
@app.route("/Hospital")
def hospital():
    return render_template("hoslogin.html")
@app.route("/Hospital/Success", methods=["POST"])
def hospitalsuccess():
    paswd=request.form.get("psw")
    try:
        hid=int(request.form.get("uname"))
    except ValueError:
        return render_template("error.html",message="Please enter a valid hospital id and try again")
    if db.execute("SELECT * FROM hospital where hid=:hid",{"hid":hid}).rowcount == 0:
        return render_template("error.html",message="No such hospital id exists! You are not registered with with us kindly registered with us!")
    hospital=db.execute("SELECT * FROM hospital where hid=:hid",{"hid":hid}).fetchone()
    if hid==hospital.hid and paswd=="1001":
        return render_template("hospital.html",hospital=hospital)
        
if __name__== "__main__":
    main()