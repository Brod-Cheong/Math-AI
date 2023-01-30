
import string
from tkinter import E
from flask import render_template,request, flash
from flask.helpers import url_for
from flask_cors import CORS, cross_origin
from application import app, db,login_manager
from PIL import Image, ImageOps, ImageEnhance
from application.models import  User,Entry,EquationEntry
from datetime import datetime
from flask import  redirect, render_template, flash, request, session
import cv2
from application.SolveEquation.ExpressionClass import Expression
from application.SolveEquation.Evaluator import Evaluator

import keras.models
from flask_login import login_required, current_user, login_user,logout_user
from flask import json, jsonify
import re
import base64
from io import BytesIO
from keras.preprocessing import image
# from tensorflow.keras.datasets.mnist import load_data
import json
import numpy as np
import requests
import pathlib, os
from application.forms import LoginForm,SignUpForm
import ast

#----------------------------------------------------------------------
#Entry Class Functions



def get_entry(id):
    try:
        entries = Entry.query.filter(Entry.id==id)
        result = entries[0]
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0  

#get all Existing Entries
def get_AllEntries():
    try:
        entries = Entry.query.all()
        print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

#get all User's entry
def get_AllUserEntries(userid):
    try:
        entries = Entry.query.filter_by(userid=userid)
        
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

def get_AllEntriesByEquationId(id):
    try:
        entries = Entry.query.filter_by(Equationid=id) 
        print(entries)
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

def get_NumberOfEntries(userid):
    try:
        entries = Entry.query.filter_by(userid=userid).count()
        return entries
    except Exception as error:
        db.session.rollback()

        flash(error,"danger") 
        return 0
def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
 
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_LimitedEntries(count):
    try:
        print(count)
        count=int(count)
        entries = Entry.query.all()[-count:]
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0


def remove_AllEntryforEquationId(id):
    try:

        delete_query = Entry.__table__.delete().where(Entry.Equationid == int(id) )
        db.session.execute(delete_query)
        db.session.commit()

    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

#Remove a certain Entry
def remove_entry(id):
    try:
        entry = Entry.query.get(id)
        os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(entry.FileName))
        os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(entry.FileName[:-5]+"_Inverted"+entry.FileName[-5:]))
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def remove_nullequations():
    try:
        entries = Entry.query.filter(Entry.Equationid.is_(None) )
        print(entries)
        for i in entries:
            print(i.FileName)
            os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(i.FileName))
            print(i.FileName[:-5]+"_Inverted"+i.FileName[-5:])
            os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(i.FileName[:-5]+"_Inverted"+i.FileName[-5:]))
        delete_query = Entry.__table__.delete().where(Entry.Equationid == None )
        db.session.execute(delete_query)
        db.session.commit()

    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

#-----------------------------------------------------------------------------
# Get all users
def get_AllUser():
    try:
        entries = User.query.all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0  

#Add a new User
def add_User(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
 
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

#Remove a user
def remove_User(id):
    try:
        entry = User.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

#get a User
def get_User(id):
    try:
        entries = User.query.filter(User.id==id)
        result = entries[0]
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0  


#----------------------------------------------------------------------
#EquationEntry Functions

#get all Equation's entry
def get_AllUserEquationEntry(userid):
    try:
        entries = EquationEntry.query.filter_by(userid=userid)
       
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0


def add_EquationEntry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
 
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_AllEquationEntries():
    try:
        entries = EquationEntry.query.all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger") 
        return 0

#Remove a certain Entry
def remove_EquationEntry(id):
    try:
        entry = EquationEntry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:


        db.session.rollback()
        flash(error,"danger")
#---------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to do that.','danger')
    return redirect(url_for('LoginPage'))

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        return redirect(url_for('LoginPage'))

@app.route('/MakePred')
def MakePred():
    if current_user.is_authenticated:
        return render_template("MakePred.html")
    else:
        return redirect(url_for('LoginPage'))




@app.route('/') #Default directory
@app.route('/LoginPage')
def LoginPage():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        Login_form=LoginForm()
        return render_template("login.html", Login_form=Login_form)

@app.route('/Login',methods=['GET','POST'])
def Login():
    Login_form=LoginForm()
    if Login_form.validate_on_submit():
        user=User.query.filter_by(Username=Login_form.LoginUsername.data).first()
        if user and user.check_password(password=Login_form.LoginPassword.data):
            login_user(user) 
            return redirect(url_for('home'))
        else:
            flash("Error, cannot proceed with Logging In","danger")
    return render_template('login.html', title="Login" ,Login_form = Login_form, index=True)



#To logout of account
@app.route("/Logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('LoginPage'))


#Sign Up for Developer use
@app.route('/SignUp')
def SignUp():
    signup_form= SignUpForm()
    return render_template("SignUp.html", signup_form=signup_form)

@app.route('/Sign_Up',methods=['GET','POST'])
def Sign_Up():
    signup_form= SignUpForm()
    db.create_all()
    if request.method == 'POST':
     
        if signup_form.validate_on_submit():
           
            try:
                existing_user = User.query.filter_by(Username=signup_form.UserName.data).first()
                if existing_user is None:
                    user=User(
                        Username= signup_form.UserName.data,
                        created_on=datetime.utcnow()
                    )
                    user.set_password(signup_form.Password.data)
                    add_User(user)
                    flash(f"Successfully Signed Up! You can login now!","success")
                else:
                    flash("Error, cannot proceed with Sign Up","danger")
            except Exception as error:
                db.session.rollback()
                flash(error,"danger")
        return render_template('SignUp.html' ,signup_form = signup_form,index=True)


#Predictions
def parseImage(imgData,username,NumberOfPastEntries):
    newEntryNumber=NumberOfPastEntries+1
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    timenow=datetime.utcnow()
    filename=("{}_{}_{}.jpeg").format(username,newEntryNumber,timenow)
    fileDirectory=("application/static/images/UserImages/{}_{}_{}.jpeg").format(username,newEntryNumber,timenow)
    with open(fileDirectory,'wb') as output:
        output.write(base64.decodebytes(imgstr))
    im = cv2.imread(fileDirectory)
    	
    grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    converted_Img_filedirectory=("/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}_{}_{}_Inverted.jpeg").format(username,newEntryNumber,timenow)
    cv2.imwrite(converted_Img_filedirectory,blackAndWhiteImage)
    return(filename,converted_Img_filedirectory)
 
def make_prediction(instances):
    data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
    print(data)
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    print(json_response)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

#server URL
url = 'https://doaa-joshbrod-dlmodel-ca2.herokuapp.com/v1/models/img_classifier:predict'

#Handles http://127.0.0.1:5000/predict
@app.route("/predict", methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def predict():
    # get data from drawing canvas and save as image
    if(current_user.is_authenticated):
        db.create_all()
        username=current_user.Username
        userId=current_user.get_id()
        NumberOfPastEntries= get_NumberOfEntries(userId)
        filename,convert_img_filedirectory=parseImage(request.get_data(),username,NumberOfPastEntries)
        
        

        img = image.img_to_array(image.load_img(convert_img_filedirectory, color_mode="grayscale", target_size=(45, 45))) / 255.
        


        img = img.reshape(1,45,45,1)
        print((img))
        print(img.shape)
        predictions = make_prediction(img)
        print(predictions)
        classes=['+','-','0','1','2','3','4','5','6','7','8', '9']
        ret = ""
        for i, pred in enumerate(predictions):
            index=np.argmax(pred)
            ret = "{}".format(classes[np.argmax(pred)])
            new_Entry= Entry(
                userid=userId,  FileName=filename,predicted_value=classes[np.argmax(pred)],
                            time_stamp=datetime.utcnow())
            result=add_entry(new_Entry)
            response = {'prediction':ret,'Probability':np.round(pred[index]*100,2)}
            return jsonify(response)


#----------------------------------------------------------------------------
#Equation Routes

#Solve Equation
@app.route("/SolveEquation", methods=['GET','POST'])
def SolveEquation(): 
    
    if request.method == 'POST':
        data=ast.literal_eval((request.get_data()).decode('utf-8'))
        print(type(data['NumberToAdd']))
        EquationExpression=Expression(data['Equation'])
        evaluator = Evaluator( "", "~", '1')
        ValidBracket,ValidOperators,fullySeperatedTokens=EquationExpression.Validate_UserInput()
        Expression_value = evaluator.evaluateSingleExpression(fullySeperatedTokens)
        # EquationExpression.BuildParseTree()
        # Expression_value=EquationExpression.EvaluateExpression()
        print(Expression_value)
        if(current_user.is_authenticated):
            db.create_all()
            userId=current_user.get_id()
            
            new_entry= EquationEntry( userid=userId, equation=data['Equation'],
                                Solved_value=Expression_value,time_stamp=datetime.utcnow())
            equationId=add_EquationEntry(new_entry)
        entries= get_LimitedEntries(data['NumberToAdd'])
        #Prepare a dictionary for json conversion
        for i in entries:
            i.set_Equationid(equationId)
            add_entry(i)
        remove_nullequations()
        return str(Expression_value)


@app.route("/getAllEquationEntry", methods=['GET'])
def getAllEquationEntries(): 
    #Get all entries data
    entries= get_AllEquationEntries()

    data=[]
    #Prepare a dictionary for json conversion
    for i in entries:

        d =     {'id'        : i.id,
                'userid'    : i.userid,
                'equation': i.equation,
                'Solved_value': i.Solved_value,
                'time_stamp': i.time_stamp}
        data.append(d)

    #Convert the data to json
    result = jsonify(data)
    return result #response back

#Remove Equation Entry

@app.route('/removeEquation', methods=['POST'])
def removeEquation():
    req = request.form
    id = req["id"]
    userId=current_user.get_id()
    remove_EquationEntry(id)
    entries=get_AllEntriesByEquationId(id)
    print(entries)
    for i in entries:
        print(i.FileName)

        os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(i.FileName))
        os.remove('/ca2-2b05-joshuabrod-web/application/static/images/UserImages/{}'.format(i.FileName[:-5]+"_Inverted"+i.FileName[-5:]))
    remove_AllEntryforEquationId(id)
    return render_template("PastPred.html",  entries = get_AllUserEquationEntry(userId) )


@app.route("/ViewImages",methods=["GET",'POST'])
def ViewImages():
    if(current_user.is_authenticated):
        req = request.form

        UserEquationID = req['id']

        UserImages=get_AllEntriesByEquationId(UserEquationID)

        return render_template("ViewImages.html",entries=UserImages)
        # return render_template("PastPred.html",EquationEntries=UserEquations,ImagesEntries=UserImages)
    else:
        return redirect(url_for('LoginPage'))


@app.route("/PastPred")
def PastPrediction():
    if(current_user.is_authenticated):
        userId=current_user.get_id()

        UserEquations=get_AllUserEquationEntry(userId)

        return render_template("PastPred.html",entries=UserEquations)
    else:
        return redirect(url_for('LoginPage'))

#----------------------------------------------------------------------

# API for User Class

@app.route("/api/getAllUser", methods=['GET','POST'])
def api_getAllUser():
    entries = get_AllUser()
    data=[]
    print(entries)
    for user in entries:
        userdata= {
            'id': user.id,
            'Username': user.Username,
            'password': user.password,
            'created_on': user.created_on
        }
        data.append(userdata)


    result=jsonify(data)
    return result


#API get entry by userid
@app.route("/api/getUser/<id>", methods=['GET'])
def api_getUser(id): 
    #retrieve the entry using id from client
    entry = get_User(int(id))
    #Prepare a dictionary for json conversion
    data = {'id'        : entry.id,
            'Username'    : entry.Username,
            'password': entry.password,
            'created_on':entry.created_on
        }

    #Convert the data to json
    result = jsonify(data)
    return result #response back
#----------------------------------------------------------------------

# API for Entry Class

#API: add entry
@app.route("/api/addEntry", methods=['POST'])
def api_addEntry(): 
    db.create_all()
    #retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    Equationid     = data['Equationid']
    FileName     = data['FileName']
    predicted_value=    data['predicted_value']  
    useraccount=get_User(data['userid'])
    login_user(useraccount)

    #create an Entry object store all data for db action
    if(current_user.is_authenticated):
        userId=current_user.get_id()
        new_entry = Entry(  userid=userId,Equationid=Equationid,FileName=FileName,
                            predicted_value=predicted_value,  
                            time_stamp=datetime.utcnow())
        add_entry(new_entry)
    #invoke the add entry function to add entry                        
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})

#API:get all entries
@app.route("/api/getAllEntry", methods=['GET'])
def api_getAllEntries(): 
    #Get all entries data
    entries= get_AllEntries()

    data=[]
    #Prepare a dictionary for json conversion
    for i in entries:

        d =     {'id'        : i.id,
                'userid'    : i.userid,
                'FileName': i.FileName,
                'Equationid':i.Equationid,
                'predicted_value': i.predicted_value,
                'time_stamp': i.time_stamp}
        data.append(d)

    #Convert the data to json
    result = jsonify(data)
    return result #response back


#API get entry by userid
@app.route("/api/getEntry/<id>", methods=['GET'])
def api_getEntry(id): 
    #retrieve the entry using id from client
    entry = get_entry(int(id))
    #Prepare a dictionary for json conversion
    data = {'id'        : entry.id,
            'userid'    : entry.userid,
            'FileName': entry.FileName,
            'Equationid':entry.Equationid,
            'predicted_value': entry.predicted_value}

    #Convert the data to json
    result = jsonify(data)
    return result #response back


#API get entry by equationid
@app.route("/api/getAllEntryEquationID/<id>", methods=['GET'])
def get_API_AllEquationEntriesID(id): 
    #Get all entries data

    entries= get_AllEntriesByEquationId(int(id))
    print(entries)
    data={
        'id': entries.id,
        'userid': entries.userid,
        'Equationid': entries.Equationid,
        'FileName': entries.FileName,
        'predicted_value': entries.predicted_value,
        'time_stamp': entries.time_stamp
    }
    print(data)
    #Convert the data to json
    result = jsonify(data)
    return result #response back

#API delete entry
@app.route("/api/deleteEntry/<id>", methods=['GET'])
def api_deleteEntry(id): 
    entry = remove_entry(id)
    return jsonify({'result':'ok'})



#----------------------------------------------------------------------

# API for Prediction

@app.route("/api/predict",methods=['POST'])
def api_predict():

    data = request.get_json()
    #Convert the data to json
    result= jsonify(data)
    return result

#----------------------------------------------------------------------

# API for EquationEntry Class

#API: get all equations
@app.route("/api/getAllEquationEntry", methods=['GET'])
def get_API_AllEquationEntries(): 
    #Get all entries data
    entries= get_AllEquationEntries()
    
    data=[]
    #Prepare a dictionary for json conversion
    for i in entries:

        d =     {'id'        : i.id,
                'userid'    : i.userid,
                'equation': i.equation,
                'Solved_value': i.Solved_value,
                'time_stamp': i.time_stamp}
        data.append(d)

    #Convert the data to json
    result = jsonify(data)
    return result #response back

#API: get equations by id
@app.route("/api/getAllEquationEntry/<id>", methods=['GET'])
def get_API_AllUserEquationEntry(id): 
    #Get all entries data
    entries= get_AllUserEquationEntry(int(id))
    
    data=[]
    #Prepare a dictionary for json conversion
    for i in entries:

        d =     {'id'        : i.id,
                'userid'    : i.userid,
                'equation': i.equation,
                'Solved_value': i.Solved_value,
                'time_stamp': i.time_stamp}
        data.append(d)

    #Convert the data to json
    result = jsonify(data)
    return result #response back


#API delete equation entry
@app.route("/api/deleteEquationEntry/<id>", methods=['GET'])
def api_deleteEquationEntry(id): 
    entry = remove_EquationEntry(int(id))
    return jsonify({'result':'ok'})

@app.route("/api/deleteNullEquation", methods=['GET'])
def api_remove_nullequations():
    entry = remove_nullequations()
    return jsonify({'result':'ok'})