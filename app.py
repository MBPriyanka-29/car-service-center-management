from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime
import yaml
import os
import itertools

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
        dateOfBirth = registerC['dateOfBirth']
        first_address = registerC['first_address']
        district = registerC['district']
        pincode = registerC['pincode']
        emailID = registerC['email']
        dl_num = registerC['dl_num']
        phone_num = registerC['phone_num']
        pswd = registerC['pswd']
        re_enter_password = registerC['re_enter_password']

        cur = mysql.connection.cursor()

        if request.form['submit_button'] == 'submit_registration':
            if customer_id and c_fname and c_lname and first_address and district and pincode and emailID and dl_num and phone_num and pswd and re_enter_password:
                if len(customer_id) == 12:
                    if len(pincode) == 6:
                        if len(dl_num) == 16:
                            if len(phone_num) == 10:
                                if pswd == re_enter_password:
                                    cur.execute("insert into customer(customer_id,c_fname,c_lname,dateOfBirth,first_address,district,pincode,dl_num,phone_num,emailID) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                                (customer_id, c_fname, c_lname, dateOfBirth, first_address, district, pincode, dl_num, phone_num, emailID))
                                    cur.execute(
                                        "insert into login_customer values(%s,%s,%s)", (customer_id, emailID, pswd))
                                    mysql.connection.commit()
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
                            flash("DL number is invalid, Try again!", 'error')
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
            cur1.execute("SELECT c_fname FROM customer WHERE emailID = %s ", (username,))
            n=cur1.fetchone()
            cname=n['c_fname']
            session['c_name']=cname

            if result > 0:
                data = cur.fetchone()
                cuid = data['customer_id']
                session['cid'] = cuid
                cpassword = data['pswd']

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
            cur1 = mysql.connection.cursor()
            cur1.execute("SELECT a_fname FROM admin WHERE emailID = %s ", (username,))
            n=cur1.fetchone()
            aname=n['a_fname']
            session['a_name']=aname
            cur = mysql.connection.cursor()
            result = cur.execute(
                "SELECT * FROM login_admin WHERE emailID = %s", (username,))

            if result > 0:
                data = cur.fetchone()
                auid = data['admin_id']
                session['aid'] = auid
                apassword = data['pswd']

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
    return render_template('dashboard_a.html',a_name=a_name)

@app.route('/addMechanics', methods=['GET', 'POST'])
def addMechanics():
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
    cur = mysql.connection.cursor()
    aid = session['aid']
    result = cur.execute("select * FROM mechanic where admin_id = %s", (aid,))
    if(result > 0):
        mech = cur.fetchall()
    else:
        flash("No Mechanics to display", 'error')
        return render_template('dashboard_a.html')

    mysql.connection.commit()
    cur.close()
    return render_template('viewMechanics.html', mech=mech)

@app.route('/dashboard_c', methods=['GET', 'POST'])
def dashboard_c():
    c_name=session['c_name']
    return render_template('dashboard_c.html',c_name=c_name)

@app.route('/selectStation', methods=['GET', 'POST'])
def selectStation():
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
            return render_template('dashboard_c.html')
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
            return render_template('dashboard_c.html')

    return render_template('serviceRequest.html')


@app.route('/serviceHistory', methods=['GET', 'POST'])
def serviceHistory():

    cur1 = mysql.connection.cursor()
    cid = session['cid']
    result_cs = cur1.execute(
        "select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and car_claims_service.customer_id=%s",(cid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("No Services added!", 'error')
        return render_template('dashboard_c.html')
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE','ADMIN REMARK','ADMIN REMARK DATE', 'STATUS OF REQUEST','REQUEST FINALISATION']
        return render_template('viewServiceRequest.html', indiservice=indiservice, headings=headings)
    return render_template('serviceHistory.html', car_service=car_service)


@app.route('/new', methods=['GET', 'POST'])
def new():

    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=0 and admin_id = %s",(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no new service requests!", 'error')
        return render_template('dashboard_a.html')
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE','ADMIN REMARK','ADMIN REMARK DATE','REQUEST FINALISATION']

        if request.method == "POST":
            print("in post")
            service = request.form
            s_status = service['s_status']
            print("s_status: ", s_status)
            buttonvalue = service['ServiceCompletedButton']
            if buttonvalue == "ServiceCompleted":
                print("Button clicked")
                if s_status == "selected":
                    status = 2
                else:
                    status = 1
                print("status", status)
                cur = mysql.connection.cursor()
                cur.execute(
                    "UPDATE service SET s_status=%s WHERE service_id=%s", (status, service_id))
                mysql.connection.commit()
                cur.close()
                flash("STATUS of request updated successfuly!", 'success')
                return redirect('/new')
        return render_template('newView.html', indiservice=indiservice, headings=headings)
    return render_template('new.html', car_service=car_service)


@app.route('/rejected', methods=['GET', 'POST'])
def rejected():

    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=1 and admin_id = %s" ,(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no rejected service requests!", 'error')
        return render_template('dashboard_a.html')
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
                        status = 2
                        cur = mysql.connection.cursor()
                        cur.execute(
                            "UPDATE service SET s_status=%s WHERE service_id=%s", (status, service_id))
                        mysql.connection.commit()
                        cur.close()
                        flash("STATUS of request updated successfuly!", 'success')
                        return redirect('/rejected')
                    else:
                        status = 1
                else:
                    return redirect('/rejected')
        return render_template('viewRejected.html', indiservice=indiservice, headings=headings)
    return render_template('rejected.html', car_service=car_service)

@app.route('/pending', methods=['GET', 'POST'])
def pending():
    cur1 = mysql.connection.cursor()
    aid = session['aid']
    result_cs = cur1.execute(
        "select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.s_status=2 and admin_id = %s",(aid,))
    if((result_cs > 0)):
        car_service = cur1.fetchall()
        # print(car_service)
    else:
        flash("There are no pending service requests!", 'error')
        return render_template('dashboard_a.html')
    cur1.close()
    if 'view' in request.args:
        service_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("select * from service,car,car_claims_service where service.service_id=car_claims_service.service_id and car.Registration_num=car_claims_service.Registration_num and service.service_id = %s", (service_id,))
        indiservice = curso.fetchall()
        headings = ['SERVICE REQUESTED ON', 'CAR NAME', 'COMAPNY', 'MODEL', 'REGISTRATION NUMBER', 'SERVICE TYPE', 'SERVICE DATE',
                    'TIME', 'SPECIFICATIONS', 'DELIVERY TYPE', 'PICKUP ADDRESS', 'PINCODE']

        if request.method == "POST":
            print("in post")
            service = request.form
            s_status = service['s_status']
            print("s_status: ", s_status)
            buttonvalue = service['ServiceCompletedButton']
            if buttonvalue == "ServiceCompleted":
                print("Button clicked")
                if s_status == "selected":
                    status = 2
                else:
                    status = 1
                print("status", status)
                cur = mysql.connection.cursor()
                cur.execute(
                    "UPDATE service SET s_status=%s WHERE service_id=%s", (status, service_id))
                mysql.connection.commit()
                cur.close()
                flash("request finalised successfuly!", 'success')
                return redirect('/new')
        return render_template('viewPending.html', indiservice=indiservice, headings=headings)
    return render_template('pending.html', car_service=car_service)



if __name__ == '__main__':
    app.run(debug=True)
