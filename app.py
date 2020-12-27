from flask import Flask, render_template, request, redirect, url_for, flash, session,json,jsonify
from flask_mysqldb import MySQL
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime
import json
import yaml
import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient  
import seaborn as sns
import shutil
  
i=2
j=100
# Making Connection 
myclient = MongoClient("mongodb://localhost:27017/")  
   
# database  
db = myclient["car_mongo"] 
   
# Created or Switched to collection  
# names: GeeksForGeeks 
Collection = db["districts"] 
Collection_rating=db["rating"]


# pip install -U Werkzeug==0.16.0

app = Flask(__name__)

app.secret_key = 'secret'
# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = db['mysql_cursorclass']
app.config['UPLOADED_PHOTOS_DEST'] = db['uploaded_photos_dest']

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')


@app.route('/registerCustomer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        # fetch form data
        registerC = request.form
        customer_id = registerC['customer_id']
        c_fname = registerC['c_fname']
        c_lname = registerC['c_lname']
        first_address = registerC['first_address']
        district = registerC['district']
        pincode = registerC['pincode']
        emailID = registerC['email']
        phone_num = registerC['phone_num']
        pswd = registerC['pswd']
        re_enter_password = registerC['re_enter_password']

        cur = mysql.connection.cursor()

        if request.form['submit_button'] == 'submit_registration':
            if customer_id and c_fname and c_lname and first_address and district and pincode and emailID and phone_num and pswd and re_enter_password:
                if len(customer_id) == 12:
                    if len(pincode) == 6:
                        if len(phone_num) == 10:
                            if pswd == re_enter_password:
                                cur.execute("insert into customer(customer_id,c_fname,c_lname,first_address,district,pincode,phone_num,emailID) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                                            (customer_id, c_fname, c_lname, first_address, district, pincode, phone_num, emailID))
                                cur.execute(
                                    "insert into login_customer values(%s,%s,%s)", (customer_id, emailID, pswd))
                                mysql.connection.commit()
                                # convert customer table to json file
                                cur.execute("select * from customer")
                               # row_headers=[x[0] for x in cur.description] #this will extract row headers
                                customer_table=cur.fetchall()
                                print(customer_table)
                                customer=[]
                                contents={}
                                for result in customer_table:
                                    contents={"customer_id":result['customer_id'], "c_fname":result['c_fname'], "c_lname":result['c_lname'], "first_address":result['first_address'], "district":result['district'], "state":result['state'], "pincode":result['pincode'],"phone_num":result['phone_num'], "emailID":result['emailID']}
                                    customer.append(contents)
                                    contents={}
                                with open('customer_json.json','w') as file:
                                    json.dump(customer,file)
                                #return jsonify(customer)
                                ######################################

                                cur.close()
                                flash(
                                    "You have registered as a customer successfully!", 'success')
                                return redirect('/login')

                            elif pswd != re_enter_password:
                                flash(
                                    "Password doesn't match, Please re-enter the same password!", 'error')
                                redirect('/registerCustomer')
                        else:
                            flash(
                                "Phone number is invalid, Try again!", 'error')
    
                    else:
                        flash("Pincode is invalid, Try again!", 'error')
                else:
                    flash("Adhaar card is invalid, Try again!", 'error')
            else:
                flash("Please fill all the details!", 'error')
    return render_template('registerCustomer.html')


@app.route('/registerAdmin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        # fetch form data
        registerA = request.form
        admin_id = registerA['admin_id']
        a_fname = registerA['a_fname']
        a_lname = registerA['a_lname']
        emailID = registerA['email']
        s_name = registerA['s_name']
        s_num = registerA['s_num']
        first_address = registerA['first_address']
        district = registerA['district']
        pincode = registerA['pincode']
        pswd = registerA['pswd']
        re_enter_password = registerA['re_enter_password']

        cur = mysql.connection.cursor()

        if request.form['submit_button'] == 'submit_registration':
            if admin_id and a_fname and a_lname and first_address and district and pincode and emailID and s_name and s_num and pswd and re_enter_password:
                if len(admin_id) == 12:
                    if len(pincode) == 6:
                        if pswd == re_enter_password:
                            cur.execute("insert into admin(admin_id,a_fname,a_lname,emailID) values(%s,%s,%s,%s)", (
                                admin_id, a_fname, a_lname, emailID))
                            cur.execute(
                                "insert into login_admin values(%s,%s,%s)", (admin_id, emailID, pswd))
                            cur.execute("insert into service_station(s_name,first_address,district,pincode,admin_id,s_num) values(%s,%s,%s,%s,%s,%s)", (
                                s_name, first_address, district, pincode, admin_id, s_num))
                            mysql.connection.commit()
                            # convert station to json file
                            cur.execute("select district from service_station")
                            # row_headers=[x[0] for x in cur.description] #this will extract row headers
                            district=cur.fetchall()
                            print(district)
                            d=[]
                            contents={}
                            for result in district:
                                contents={"district:":result['district']}
                                d.append(contents)
                                contents={}
                            with open('district_json.json','w') as file:
                                json.dump(d,file)
                            
                            ######################################
                            cur.close()
                            flash(
                                "You have registered as an admin successfully!", 'success')
                            return redirect('/login')
                        elif pswd != re_enter_password:
                            flash(
                                "Password doesn't match, Please re-enter the same password!", 'error')
                            redirect('/registerAdmin')
                    else:
                        flash("Pincode is invalid, Try again!", 'error')
                else:
                    flash("Adhaar card is invalid, Try again!", 'error')
            else:
                flash("Please fill all the details!", 'error')
    return render_template('registerAdmin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password_candidate = request.form['password']

        if request.form['typeofuser'] == "Customer":
            cur = mysql.connection.cursor()
            result = cur.execute(
                "SELECT * FROM login_customer WHERE emailID = %s ", (username,))
            cur1 = mysql.connection.cursor()
           
            if result > 0:
                data = cur.fetchone()
                cuid = data['customer_id']
                session['cid'] = cuid
                cpassword = data['pswd']
                cur1.execute("SELECT c_fname FROM customer WHERE emailID = %s ", (username,))
                n=cur1.fetchone()
                cname=n['c_fname']
                session['c_name']=cname
                if cpassword == password_candidate:
                    return redirect(url_for('dashboard_c'))

                else:
                    flash("Incorrect password !", 'error')
                    return render_template('login.html')

            else:
                flash('Username entered is incorrect! Try again.', 'error')
                cur.close()
                return render_template('login.html')

        else:
            
            cur = mysql.connection.cursor()
            result = cur.execute(
                "SELECT * FROM login_admin WHERE emailID = %s", (username,))

            if result > 0:
                data = cur.fetchone()
                auid = data['admin_id']
                session['aid'] = auid
                apassword = data['pswd']
                cur1 = mysql.connection.cursor()
                cur1.execute("SELECT a_fname FROM admin WHERE emailID = %s ", (username,))
                n=cur1.fetchone()
                aname=n['a_fname']
                session['a_name']=aname
                cur1.execute("SELECT s_name FROM service_station WHERE admin_id = %s ", (auid,))
                n=cur1.fetchone()
                session['a_station']=n['s_name']
                print(session['a_station'])

                if apassword == password_candidate:
                    return redirect(url_for('dashboard_a'))

                else:
                    flash("Incorrect password !", 'error')
                    return render_template('login.html')

            else:
                flash('Username entered is incorrect! Try again.', 'error')
                cur.close()
                return render_template('login.html')

    return render_template('login.html')


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        fpswddata = request.form
        mail = fpswddata['emailID']
        ipswd = fpswddata['password']
        re_entered_password = fpswddata['repassword']

        cur = mysql.connection.cursor()

        if ipswd == re_entered_password:
            if fpswddata['typeofuser'] == "Customer":
                result = cur.execute(
                    "SELECT * FROM login_customer WHERE emailID = %s", (mail,))
                if result > 0:
                    cur.execute(
                        "update login_customer set pswd = %s where emailID = %s", (ipswd, mail))
                else:
                    flash("E-mail ID doesn't exist !", 'error')
                    return redirect('/forgotpassword')
            else:
                result = cur.execute(
                    "SELECT * FROM login_admin WHERE emailID = %s", (mail,))
                if result > 0:
                    cur.execute(
                        "update login_admin set pswd = %s where emailID = %s", (ipswd, mail))
                    flash("Password updated! !", 'success')
                else:
                    flash("E-mail ID doesn't exist !", 'error')
                    return redirect('/forgotpassword')
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        else:
            flash("Password doesn't match !", 'error')

    return render_template('forgot_password.html')


@app.route('/dashboard_a', methods=['GET', 'POST'])
def dashboard_a():
    a_name=session['a_name']
    aid=session['aid']
    station=session['a_station']
    counts=[]
    cur = mysql.connection.cursor()
    print(aid)
    
    
    # total requests recieved
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    counts.append(count)

    # new service requests
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s and service.s_status=0 and service.admin_status=0",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    counts.append(count)

    
    # rejected requests
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s and service.s_status=1 and service.admin_status=0",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    print(count)
    counts.append(count)

    # approved requests
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s and service.s_status=2 and service.admin_status=0",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    print(count)
    counts.append(count)

    # pending (waiting for finalisation)
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s and service.s_status=2 and service.admin_status=0",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    print(count)
    counts.append(count)

    # completed 
    result_cs = cur.execute("select count(service.admin_id) from service where service.admin_id=%s and service.s_status=2 and service.admin_status=2",(aid,))
    n=cur.fetchone()
    count=n['count(service.admin_id)']
    print(count)
    counts.append(count)
    
    if request.method=="POST":
        bt=request.form
        buttonvalue=bt['button']

        if buttonvalue=="new":
            return redirect(url_for('new'))
        elif buttonvalue=="rejected":
            return redirect(url_for('rejected'))
        elif buttonvalue=="pending":
            return redirect(url_for('pending'))
        elif buttonvalue=="completed":
            return redirect(url_for('completed'))
    return render_template('dashboard_a.html',a_name=a_name,count=counts,station=station)

@app.route('/addMechanics', methods=['GET', 'POST'])
def addMechanics():
    a_name=session['a_name']
    if request.method == 'POST':
        mechanic = request.form
        m_fname = mechanic['m_fname']
        m_lname = mechanic['m_lname']
        gender = mechanic['gender']
        phone_num = mechanic['phone_num']

        if m_fname and m_lname and gender and phone_num:
            cur = mysql.connection.cursor()
            aid = session['aid']
            cur.execute("insert into mechanic(m_fname,m_lname,phone_num,admin_id,gender) values(%s,%s,%s,%s,%s)",
                        (m_fname, m_lname, phone_num, aid, gender))
            mysql.connection.commit()
            cur.close()
            flash('Mechanic added successfully!', 'success')
        else:
            flash('Enter all details!', 'error')
    return render_template('addMechanics.html')


@app.route('/viewMechanics', methods=['GET', 'POST'])
def viewMechanics():
    a_name=session['a_name']
    cur = mysql.connection.cursor()
    aid = session['aid']
    result = cur.execute("select * FROM mechanic where admin_id = %s", (aid,))
    if(result > 0):
        mech = cur.fetchall()
    else:
        flash("No Mechanics to display", 'error')
        return redirect(url_for('dashboard_a'))

    mysql.connection.commit()
    cur.close()
    return render_template('viewMechanics.html', mech=mech)

@app.route('/dashboard_c', methods=['GET', 'POST'])
def dashboard_c():
    cid=session['cid']
    c_name=session['c_name']
    counts=[]
    cur = mysql.connection.cursor()
    
    # requested
    result_cs = cur.execute("select count(car.customer_id) from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s",(cid,))
    n=cur.fetchone()
    count=n['count(car.customer_id)']
    counts.append(count)
    
    # completed
    result_cs = cur.execute("select count(car.customer_id) from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s and service.admin_status=2",(cid,))
    n=cur.fetchone()
    count=n['count(car.customer_id)']
    print(count)
    counts.append(count)

    #waiting for approval
    result_cs = cur.execute("select count(car.customer_id) from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s and service.s_status=0",(cid,))
    n=cur.fetchone()
    count=n['count(car.customer_id)']
    print(count)
    counts.append(count)

    #waiting bill
    result_cs = cur.execute("select count(car.customer_id) from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s and service.admin_status=0 and service.s_status=2",(cid,))
    n=cur.fetchone()
    count=n['count(car.customer_id)']
    print(count)
    counts.append(count)

    #rejected
    result_cs = cur.execute("select count(car.customer_id) from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s and service.s_status=1",(cid,))
    n=cur.fetchone()
    count=n['count(car.customer_id)']
    print(count)
    counts.append(count)
    print(counts)
    
    if request.method=="POST":
      #  bt=request.form
      #  buttonvalue=bt['button']
        return redirect(url_for('serviceHistory'))
        cur.close()
    return render_template('dashboard_c.html',c_name=c_name,count=counts)

@app.route('/selectStation', methods=['GET', 'POST'])
def selectStation():
    c_name=session['c_name']
    cur = mysql.connection.cursor()
    res=cur.execute("SELECT station_id,s_name,district,first_address,pincode FROM service_station ORDER BY district")
    if res>0:
        stations=cur.fetchall()
    cur.close()
    if request.method=="POST":
        s=request.form
        s_name=s['s_name']
        cur = mysql.connection.cursor()
        res=cur.execute("SELECT admin_id FROM service_station WHERE s_name=%s",(s_name,))
        if res>0:
            a=cur.fetchone()
            admin=a['admin_id']
        flash("Service station selected successfully. Enter request details!",'success')
        return redirect(url_for('serviceRequest',admin=admin))
    return render_template('selectStation.html',stations=stations)

@app.route('/serviceRequest/<admin>', methods=['GET', 'POST'])
def serviceRequest(admin):
    c_name=session['c_name']
    if request.method == 'POST':
        service = request.form
        car_name = service['car_name']
        company = service['company']
        model = service['model']
        Registration_num = service['Registration_num']
        s_name = service['s_name']
        Specifications = service['specs']
        s_date = service['service_date']
        s_time = service['service_time']
        delivery_type = service['delivery_type']

        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        #print("deli "+delivery_type)
        print("dt_string "+formatted_date)
        # service_request_date=dt_string

        #print("in service request")

        cur = mysql.connection.cursor()
        if delivery_type == 'pickup':
            address = service['address']
            pincode = service['pincode']
            cid = session['cid']
            cur.execute("insert into car(car_name,company,model,Registration_num,customer_id) values(%s,%s,%s,%s,%s)",
                        (car_name, company, model, Registration_num, cid))
            mysql.connection.commit()
            cur.execute("insert into service(s_name,s_date,s_time,Specifications,delivery_type,address,pincode,customer_id,service_request_date,admin_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (s_name, s_date, s_time, Specifications, delivery_type, address, pincode, cid, formatted_date,admin))
            mysql.connection.commit()
            cur.execute(
                "SELECT service_id FROM service WHERE service_request_date=%s", (formatted_date,))
            sid = cur.fetchone()
            #print('service id is .....................')
            # print(sid['service_id'])
            cur.execute("insert into car_claims_service(service_id,Registration_num,customer_id) values(%s,%s,%s)",
                        (sid['service_id'], Registration_num, cid))

            mysql.connection.commit()

            cur.close()
            flash(
                'Service requested successfully!You chose to pick up car from your location.', 'success')
            flash('Please wait for the approval from service station!', 'success')
            return redirect(url_for('dashboard_c'))
        else:
            cid = session['cid']
            cur.execute("insert into car(car_name,company,model,Registration_num,customer_id) values(%s,%s,%s,%s,%s)",
                        (car_name, company, model, Registration_num, cid))
            mysql.connection.commit()
            cur.execute("insert into service(s_name,s_date,s_time,Specifications,delivery_type,customer_id,service_request_date,admin_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (s_name, s_date, s_time, Specifications, delivery_type, cid, formatted_date,admin))
            mysql.connection.commit()
            cur.execute(
                "SELECT service_id FROM service WHERE service_request_date=%s", (formatted_date,))
            sid = cur.fetchone()
            cur.execute("insert into car_claims_service(service_id,Registration_num,customer_id) values(%s,%s,%s)",
                        (sid['service_id'], Registration_num, cid))
            mysql.connection.commit()
            cur.close()
            flash(
                'Service requested successfully!You chose to drop your car at the service station.', 'success')
            flash('Please wait for the approval from service station!', 'success')
            return redirect(url_for('dashboard_c'))

    return render_template('serviceRequest.html')


@app.route('/serviceHistory', methods=['GET', 'POST'])
def serviceHistory():
    c_name=session['c_name']
    cur1 = mysql.connection.cursor()
    cid = session['cid']
    result_cs = cur1.execute(
        "select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s",(cid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("No Services added!", 'error')
        return redirect(url_for('dashboard_c'))
     
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchone()
        
        curso.execute("select * from service,service_station where service.admin_id=service_station.admin_id and service.admin_id=%s",(indiservice['admin_id'],))
        station=curso.fetchone()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE','ADMIN REMARK','ADMIN REMARK DATE', 'STATUS OF REQUEST','REQUEST FINALISATION']
        if indiservice['mechanic_id']!="none":
            curso.execute("select * from mechanic where mechanic_id=%s",(indiservice['mechanic_id'],))
            mechanic=curso.fetchone()
            print(mechanic)
            curso.execute("select service.feedback from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
            
           # curso.execute("select service.feedback from service,service_station where service.admin_id=service_station.admin_id and service.admin_id=%s",(indiservice['admin_id'],))
            feedback=curso.fetchone()
            #Collection_rating=db["rating"]
            print(feedback)
            print(feedback['feedback'])
            if feedback['feedback']==0:
                if request.method == 'POST':
                    star = request.form
                    rating=star['rate']
                    buttonvalue=star['submit_button']
                    print(buttonvalue)
                    print(rating)
                    Collection_rating.insert({'admin_id': indiservice['admin_id'], 'rating': rating,'service_id':service_id})
                    curso.execute("update service set feedback=1 where service_id=%s",(service_id,))
                    mysql.connection.commit()
                    flash("Feedback submitted","success")
                    return redirect('/dashboard_c')
           
            return render_template('viewServiceRequest.html', s=indiservice, headings=headings,station=station,mechanic=mechanic,feedback=feedback)
        return render_template('viewServiceRequest.html', s=indiservice, headings=headings,station=station)
    return render_template('serviceHistory.html', car_service=car_service)


@app.route('/new', methods=['GET', 'POST'])
def new():
    a_name=session['a_name']
    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=0 and admin_id = %s",(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no new service requests!", 'error')
        return redirect(url_for('dashboard_a'))
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE','ADMIN REMARK','ADMIN REMARK DATE','REQUEST FINALISATION']
        r=curso.execute("select m_fname,mechanic_id from mechanic where mechanic.m_status=0 and mechanic.admin_id = %s", (aid,))
        
        if r>0:
            mech= curso.fetchall()
            if request.method == "POST":
                service = request.form
                s_status = service['s_status']
                mechanic_id=service['mechanic_id']
                buttonvalue = service['ServiceCompletedButton']
                if buttonvalue == "ServiceCompleted":
                    if s_status == "selected":
                        status = 2
                        cur1 = mysql.connection.cursor()
                        cur1.execute("UPDATE mechanic set mechanic.m_status=1 where mechanic.mechanic_id=%s",(mechanic_id,))
                        mysql.connection.commit()
                        cur = mysql.connection.cursor()
                        cur.execute("UPDATE car SET car.mechanic_id=%s where car.Registration_num=(SELECT car.Registration_num from car_claims_service  where car_claims_service.Registration_num=car.Registration_num and car_claims_service.service_id=%s)",(mechanic_id,service_id))
                        mysql.connection.commit()
                        flash("Mehchanic is assigned!", 'success')
                    else:
                        status = 1
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "UPDATE service SET s_status=%s WHERE service_id=%s", (status, service_id))
                    mysql.connection.commit()
                    cur.close()
                    cur1.close()
                    flash("STATUS of request updated successfuly!", 'success')
                    return redirect('/new')
            return render_template('newView.html', indiservice=indiservice, headings=headings,mech=mech)
            
        else:
            flash("No mechanics available to provide service! Either enter a new mechanic, or wait for vacancy of the exisiting one!","error")
            return redirect(url_for("dashboard_a"))
    return render_template('new.html', car_service=car_service)


@app.route('/rejected', methods=['GET', 'POST'])
def rejected():
    a_name=session['a_name']
    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=1 and admin_id = %s" ,(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no rejected service requests!", 'error')
        return redirect(url_for('dashboard_a'))
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE', 'ADMIN REMARK','ADMIN REMARK DATE','STATUS OF REQUEST','REQUEST FINALISATION']

        if request.method == "POST":
            service = request.form
            check = service['check']
            buttonvalue = service['update']
            if buttonvalue == "update":
                if check == "yes":
                    s_status = service['s_status']
                    if s_status == "selected":
                        status = 0
                        cur = mysql.connection.cursor()
                        cur.execute(
                            "UPDATE service SET s_status=%s WHERE service_id=%s", (status, service_id))
                        mysql.connection.commit()
                        cur.close()
                        flash("STATUS of request updated successfuly!", 'success')
                        return redirect('/new')
                    else:
                        status = 1
                else:
                    return redirect('/rejected')
        return render_template('viewRejected.html', indiservice=indiservice, headings=headings)
    return render_template('rejected.html', car_service=car_service)

@app.route('/pending', methods=['GET', 'POST'])
def pending():
    a_name=session['a_name']
    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute(
        "select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=2 and service.admin_status=0 and admin_id = %s",(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no pending service requests!", 'error')
        return redirect(url_for('dashboard_a'))
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE']
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
       # curso.execute("UPDATE bill,pays SET bill.bill_date=%s where bill.bill_id = pays.bill_id and  pays.admin_id=%s and pays.service_id=%s",(formatted_date,aid,indiservice[0]['service_id']))
        #mysql.connection.commit()
        #curso.execute("select * from pays,bill where bill.bill_id=pays.bill_id and pays.admin_id=%s and pays.service_id=%s",(aid,indiservice[0]['service_id']))
        #bill=curso.fetchall()
        
        if request.method == "POST":
            service = request.form
            service_amount=service['service_amount']
            admin_remark=service['admin_remark']
            additional_parts=service['additional_parts']
            other_amount=service['other_amount']
            admin_status = service['admin_status']
            buttonvalue = service['ServiceCompletedButton']
            if buttonvalue == "ServiceCompleted":
                if admin_status == "completed":
                    status = 2
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE service SET admin_remark=%s,admin_status=%s,service_amount=%s,additional_parts=%s,other_amount=%s,bill_date=%s WHERE service_id=%s", (admin_remark,status,service_amount,additional_parts,other_amount,formatted_date,service_id))
                    mysql.connection.commit()
                    cur.execute("SELECT SUM(service_amount+additional_parts+other_amount) from service WHERE service_id=%s",(service_id,))
                    total=cur.fetchone()
                    final_amount=total['SUM(service_amount+additional_parts+other_amount)']
                    print("final_amount {}".format(final_amount))
                    cur.execute("UPDATE service SET final_amount=%s WHERE service_id=%s", (final_amount,service_id))
                    mysql.connection.commit()
                    cur.execute("UPDATE mechanic SET mechanic.m_status=0 WHERE mechanic.mechanic_id=(SELECT car.mechanic_id FROM car,car_claims_service where car_claims_service.Registration_num=car.Registration_num and car_claims_service.service_id=%s)",(service_id,))
                    mysql.connection.commit()
                    cur.close()
                    flash("Request finalised successfuly!", 'success')
                    return redirect('/pending')
                else:
                    status = 1
                    flash("request not finalised!", 'error')
                    return redirect('/pending')
        return render_template('viewPending.html', indiservice=indiservice, headings=headings)
    return render_template('pending.html', car_service=car_service)

@app.route('/completed', methods=['GET', 'POST'])
def completed():
    a_name=session['a_name']
    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.admin_status=2 and admin_id = %s",(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
    else:
        flash("There are no completed services in your station!", 'error')
        return redirect(url_for('dashboard_a'))
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        curso.execute("select * from service,customer where customer.customer_id=service.customer_id and service.service_id = %s", (service_id,))
        customer=curso.fetchone()
        print(customer)
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE','ADMIN REMARK','ADMIN REMARK DATE','REQUEST FINALISATION']
        return render_template('viewCompleted.html', indiservice=indiservice, headings=headings,customer=customer)
    return render_template('completed.html', car_service=car_service)

@app.route('/district_vs_count', methods=['GET', 'POST'])
def district_vs_count():

    '''
    # Making Connection 
    myclient = MongoClient("mongodb://localhost:27017/")  
    
    # database  
    db = myclient["car_mongo"] 
    
    # Created or Switched to collection  
    # names: GeeksForGeeks 
    Collection = db["trial"] 
    '''
    global i
    print(i)
   # img_path="static/images/district_vs_count/output"+str(i)+".png"
   # os.remove(img_path)

    
    d='static/images/district_vs_count'
    filesToRemove = [os.path.join(d,f) for f in os.listdir(d)]
    for f in filesToRemove:
        os.remove(f) 
    
    '''
    shutil.rmtree('static/images/district_vs_count') 
    parent_dir="static/images"
    directory="district_vs_count"
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path)
    '''
    #img_path_rm="static/images/district_vs_count/output"+str(i)+".png"
    #os.remove(img_path_rm)
    x=Collection.delete_many({})
    #
    # Loading or Opening the json file 
    with open('district_json.json') as file: 
        print("Reading file")
        file_data = json.load(file) 
        
    # Inserting the loaded data in the Collection 
    # if JSON contains data more than one entry 
    # insert_many is used else inser_one is used 
    if isinstance(file_data, list): 
        Collection.insert_many(file_data)   
    else: 
        Collection.insert_one(file_data)
    print("In mongo")

    df = pd.DataFrame(list(Collection.find()))
    print(df)
    sns_plot=sns.countplot(y='district:',data=df)
    figure = sns_plot.get_figure()    
    #figure.savefig('svm_conf.png', dpi=400)
    i=i+1
    d='static/images/district_vs_count'
    output_file=str(i)+".jpg"
    img_path=os.path.join(d,output_file)
   # img_path="static/images/district_vs_count/output"+str(i)+".png"
   # print()
    figure.savefig(img_path)
    #return "mongo"
   # print("hello")
    #img_path="static/images/district_vs_count/output{}.png".format(i)
    return render_template('district_vs_count.html',name = 'output',url=img_path)

@app.route('/admin_ratings', methods=['GET', 'POST'])
def admin_ratings():
    flag=0
    global j
    aid=session['aid']
    cur1 = mysql.connection.cursor()
    result_cs = cur1.execute("select feedback from service where admin_id = %s",(aid,))
    feedback=cur1.fetchall()
    for f in feedback:
        if f['feedback']==1:
            flag=1
    if flag==1:
        d='static/images/rate'
        filesToRemove = [os.path.join(d,f) for f in os.listdir(d)]
        for f in filesToRemove:
            os.remove(f) 
        df = pd.DataFrame(list(Collection_rating.find( { "admin_id": aid })))
    # df = pd.concat([data.drop(['rating'], axis=1), data['rating'].apply(pd.Series)], axis=1)
        print(df)
        
        sns_plot=sns.countplot(x='rating',data=df)
        figure = sns_plot.get_figure()    
        #figure.savefig('svm_conf.png', dpi=400)
        j=j+1
        d='static/images/rate'
        output_file=str(j)+".jpg"
        img_path=os.path.join(d,output_file)
    # img_path="static/images/district_vs_count/output"+str(i)+".png"
    # print()
        figure.savefig(img_path)
        return render_template('admin_ratings.html',url=img_path)
    else:
        flash("No feedback recieved!","error")
        return redirect('/dashboard_a')
    return render_template('admin_ratings.html')
if __name__ == '__main__':
    app.run(debug=True)
