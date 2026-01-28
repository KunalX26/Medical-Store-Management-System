from flask import Flask,render_template,request,redirect,url_for,session

from werkzeug.utils import secure_filename
import pymysql

from MyLib import *

import time
import os

app = Flask(__name__)
app.secret_key='secret key'
app.config['UPLOAD_FOLDER'] = './static/images'






@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        medname=request.form['T1']
        cur=create_connection()
        sql="select * from medical_medicine where Medicine_Name LIKE '%"+medname+"%'"
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            data=cur.fetchall()
            return render_template('Welcome.html',data=data,mname=medname)
        else:
            return render_template('Welcome.html',msg="No medicine found",mname=medname)
    else:
        return render_template('Welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['T1']
        password = request.form['T2']
        cn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='vgt',
            autocommit=True
        )
        cur = cn.cursor()
        sql = "select * from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n==1:
            data=cur.fetchone()
            ut=data[2] #Fetch usertype from index 2
            #Create Session
            session["email"]=email
            session["usertype"]=ut
            if ut=="admin":
                return redirect(url_for('adminhome'))
            elif ut=="medical":
                return redirect(url_for('medicalhome'))
            else:
                return render_template('LoginForm.html', msg="Contact to Admin")
        else:
            return render_template('LoginForm.html', msg="Either Email or Password is incorrect")
    else:
        return render_template('LoginForm.html')


@app.route('/auth_error')
def auth_error():
    return render_template('AuthError.html')


@app.route('/adminhome')
def adminhome():
    #Check the session
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            data=admindata(e1)
            photo=check_photo(e1)
            if data==None:
                return render_template('AdminHome.html', msg="No Data Found")
            else:
                return render_template('AdminHome.html', photo=photo, data=data)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method=="POST":
                cur=create_connection()
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                sql="update admindata set name='"+name+"', address='"+address+"', contact=' "+contact+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('AdminProfile.html', msg="Data Saved")
                else:
                    return render_template('AdminProfile.html', msg="Data Not Saved")
            else:
                cur=create_connection()
                sql="select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('AdminProfile.html', data=data)
                else:
                    return render_template('AdminProfile.html', msg="No Data Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_pass_admin', methods=['GET', 'POST'])
def change_pass_admin():
    if "email" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == 'POST':
                op=request.form['T1']
                np=request.form['T2']
                email=session["email"]
                cn = pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur = cn.cursor()
                sql="update logindata set password='"+np+"' where email='"+email+"'and password='"+op+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Password changed successfully"
                    return render_template('ChangePassAdmin.html', msg=msg)
                else:
                    msg="Password not changed successfully"
                    return render_template('ChangePassAdmin.html', msg=msg)
            else:
                return render_template('ChangePassAdmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medicalhome')
def medicalhome():
    #Check the session
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut == "medical":
            data = medicaldata(e1)
            photo = check_photo(e1)
            if data==None:
                return render_template('MedicalHome.html', msg="No Data Found")
            else:
                return render_template('MedicalHome.html', photo=photo, data=data)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medical_profile', methods=['GET', 'POST'])
def medical_profile():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="medical":
            if request.method=="POST":
                cur=create_connection()
                name=request.form['T1']
                owner=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                lno=request.form['T5']
                sql="update medicaldata set Medical_Name='"+name+"', Owner_Name='"+owner+"', Address=' "+address+"', Contact='"+contact+"', Licence_No='"+lno+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('MedicalProfile.html', msg="Data Saved")
                else:
                    return render_template('MedicalProfile.html', msg="Data Not Saved")
            else:
                cur=create_connection()
                sql="select * from medicaldata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('MedicalProfile.html', data=data)
                else:
                    return render_template('MedicalProfile.html', msg="No Data Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_pass_medical', methods=['GET', 'POST'])
def change_pass_medical():
    if "email" in session:
        ut=session["usertype"]
        if ut=="medical":
            if request.method == 'POST':
                op=request.form['T1']
                np=request.form['T2']
                email=session["email"]
                cn = pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur = cn.cursor()
                sql="update logindata set password='"+np+"' where email='"+email+"'and password='"+op+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="Password changed successfully"
                    return render_template('ChangePassMedical.html', msg=msg)
                else:
                    msg="Password not changed successfully"
                    return render_template('ChangePassMedical.html', msg=msg)
            else:
                return render_template('ChangePassMedical.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/logout')
def logout():
    if "email" in session or "usertype" in session:
        session.pop("email")
        session.pop("usertype")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/admin_reg', methods=['GET', 'POST'])
def admin_reg():
    if request.method == 'POST':
        print('This is a post request')
        #receive form data
        name=request.form['T1']
        address=request.form['T2']
        contact=request.form['T3']
        email=request.form['T4']
        password=request.form['T5']
        usertype="admin"
        cn=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='vgt',
            autocommit=True
        )
        cur=cn.cursor()
        s1="insert into admindata values('"+name+"','"+address+"','"+contact+"','"+email+"')"
        s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
        try:
            cur.execute(s1)
            n1=cur.rowcount
            cur.execute(s2)
            n2=cur.rowcount
            if n1==1 and n2==1:
                msg="Data saved and Login created"
            elif n1==1:
                msg="Only Data saved"
            elif n2==1:
                msg="Only Login created"
            else:
                msg="No Data saved and no Login created"

        except pymysql.err.IntegrityError:
            msg="Already registered, use another email"
        return render_template('AdminReg.html', vgt=msg)
    else:
        #print("This is GET post")
        return render_template('AdminReg.html')


@app.route('/show_admins')
def show_admins():
    cn=pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        db='vgt',
        port=3306,
        autocommit=True
    )
    cur=cn.cursor()
    sql="select * from admindata"
    cur.execute(sql)
    n=cur.rowcount
    if n>0:
        data=cur.fetchall()
        return render_template('AdminList.html', vgt=data)
    else:
        msg="No Data Found"
        return render_template('AdminList.html', msg=msg)


@app.route('/medical_reg', methods=['GET', 'POST'])
def medical_reg():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
                if request.method == 'POST':
                    print('This is a post request')
                    #receive form data
                    name=request.form['T1']
                    owner=request.form['T2']
                    address=request.form['T3']
                    contact=request.form['T4']
                    lno=request.form['T5']
                    email=request.form['T6']
                    password=request.form['T7']
                    usertype="medical"
                    cn=pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='',
                        db='vgt',
                        autocommit=True
                    )
                    cur=cn.cursor()
                    s1="insert into medicaldata values('"+name+"','"+owner+"','"+address+"','"+contact+"','"+lno+"','"+email+"')"
                    s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                    msg=""
                    try:
                        cur.execute(s1)
                        n1=cur.rowcount
                        cur.execute(s2)
                        n2=cur.rowcount

                        if n1==1 and n2==1:
                            msg="Data saved and Login created"
                        elif n1==1:
                            msg="Only Data saved"
                        elif n2==1:
                            msg="Only Login created"
                        else:
                            msg="No Data saved and no Login created"
                    except pymysql.err.IntegrityError:
                        msg="Already registered, use another email"
                    return render_template('MedicalReg.html', vgt=msg)
                else:
                    #print("This is GET post")
                    return render_template('MedicalReg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/show_medicals')
def show_medicals():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            cn=pymysql.connect(
                host='localhost',
                user='root',
                passwd='',
                db='vgt',
                port=3306,
                autocommit=True
            )
            cur=cn.cursor()
            sql="select * from medicaldata "
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('MedicalList.html', vgt=data)
            else:
                msg="No Data Found"
                return render_template('MedicalList.html', msg=msg)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_medical', methods=['GET', 'POST'])
def edit_medical():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut== "admin":
            if request.method == 'POST':
                email=request.form['H1']
                cn=pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur=cn.cursor()
                sql="select * from medicaldata where Email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('EditMedical.html', vgt=data)
                else:
                    return render_template('EditMedical.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicals'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_medical1', methods=['GET', 'POST'])
def edit_medical1():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut== "admin":
            if request.method == 'POST':
                a=request.form['T1']
                owner_name=request.form['T2']
                address=request.form['T3']
                contact = request.form['T4']
                licence_no=request.form['T5']
                email=request.form['T6']
                cn=pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur=cn.cursor()
                sql="update medicaldata set Medical_Name='"+a+"',Owner_Name='"+owner_name+"',Address='"+address+"',Contact='"+contact+"',Licence_No='"+licence_no+"' where Email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    return render_template('EditMedical1.html',msg="Data Updated")
                else:
                    return render_template('EditMedical1.html',msg="No Changes Detected")
            else:
                return redirect(url_for('show_medicals'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_medical', methods=['GET', 'POST'])
def delete_medical():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            if request.method == 'POST':
                email=request.form['H1']
                cn=pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur=cn.cursor()
                sql="select * from medicaldata where Email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('DeleteMedical.html', vgt=data)
                else:
                    return render_template('DeleteMedical.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicals'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_medical1', methods=['GET', 'POST'])
def delete_medical1():
    if "email" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method == 'POST':
                email = request.form['T1']
                cn = pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    db='vgt',
                    port=3306,
                    autocommit=True
                )
                cur = cn.cursor()
                s1 = "delete from medicaldata where Email='" + email + "'"
                s2 = "delete from logindata where Email='" + email + "'"
                cur.execute(s1)
                cur.execute(s2)
                n1 = cur.rowcount
                n2 = cur.rowcount
                if n1==1 and n2==1:
                    return render_template('DeleteMedical1.html', msg="Data Deleted")
                else:
                    return render_template('DeleteMedical1.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicals'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medicine_reg', methods=['GET', 'POST'])
def medicine_reg():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut == "medical":
            if request.method == 'POST':
                print('This is a post request')
                # receive form data
                name = request.form['T1']
                type = request.form['T2']
                company = request.form['T3']
                licence = request.form['T4']
                price = request.form['T5']
                description = request.form['T6']
                cn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='vgt',
                    autocommit=True
                )
                cur = cn.cursor()
                s1 = "insert into medicinedata values(0,'" + name + "','" + type + "','" + company + "','" + licence + "','" + price + "','" + description + "','"+e1+"')"
                msg = ""
                try:
                    cur.execute(s1)
                    n = cur.rowcount

                    if n>0:
                        msg = "Medicine Data Saved"
                    else:
                        msg = "Medicine Data Not Saved"
                except pymysql.err.IntegrityError:
                    msg = "Medicine already registered, add another medicine"
                return render_template('MedicineReg.html', vgt=msg)
            else:
                #print("This is GET post")
                return render_template('MedicineReg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route('/show_medicines')
def show_medicines():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut=="medical":
            cur = create_connection()
            sql="select * from medicinedata where Medical_Email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('MedicineList.html', vgt=data)
            else:
                msg="No Data Found"
                return render_template('MedicineList.html', msg=msg)
        else:
            return redirect(url_for('auth_error'))
    else:
            return redirect(url_for('auth_error'))


@app.route('/edit_medicine', methods=['GET', 'POST'])
def edit_medicine():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut=="medical":
            if request.method == 'POST':
                id=request.form['H1']
                cur = create_connection()
                sql="select * from medicinedata where Med_Id='"+id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('EditMedicine.html', vgt=data)
                else:
                    return render_template('EditMedicine.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/edit_medicine1', methods=['GET', 'POST'])
def edit_medicine1():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut=="medical":
            if request.method == 'POST':
                id=request.form['T0']
                a=request.form['T1']
                type=request.form['T2']
                company=request.form['T3']
                licence = request.form['T4']
                price=request.form['T5']
                description=request.form['T6']
                cur = create_connection()
                sql="update medicinedata set Medicine_Name='"+a+"',Medicine_Type='"+type+"',Medicine_Company='"+company+"',Medicine_Licence_No='"+licence+"',Medicine_Unit_Price='"+price+"',Medicine_Description='"+description+"' where Med_Id='"+id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    return render_template('EditMedicine1.html',msg="Data Updated")
                else:
                    return render_template('EditMedicine1.html',msg="Data Not Updated")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_medicine', methods=['GET', 'POST'])
def delete_medicine():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut=="medical":
            if request.method == 'POST':
                id=request.form['H1']
                cur = create_connection()
                sql="select * from medicinedata where Med_Id='"+id+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('DeleteMedicine.html', vgt=data)
                else:
                    return render_template('DeleteMedicine.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/delete_medicine1', methods=['GET', 'POST'])
def delete_medicine1():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if ut=="medical":
            if request.method == 'POST':
                id = request.form['T1']
                cur = create_connection()
                sql = "delete from medicinedata where Med_Id='"+id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n>0:
                    return render_template('DeleteMedicine1.html', msg="Data Deleted")
                else:
                    return render_template('DeleteMedicine1.html', msg="No Data Found")
            else:
                return redirect(url_for('show_medicines'))
        else:
            return redirect(url_for('auth_error'))
    else:
         return redirect(url_for('auth_error'))


@app.route('/medical_stores')
def medical_stores():

        cn=pymysql.connect(
            host='localhost',
            user='root',
            passwd='',
            db='vgt',
            port=3306,
            autocommit=True
        )
        cur=cn.cursor()
        sql="select * from medicaldata "
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            data=cur.fetchall()
            return render_template('MedicalStores.html', vgt=data)
        else:
            msg="No Data Found"
            return render_template('MedicalStores.html', msg=msg)


@app.route('/adminphoto')
def adminphoto():
    return render_template('UploadAdminPhoto.html')

@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('UploadAdminPhoto1.html', result="success")
                        else:
                            return render_template('UploadAdminPhoto1.html', result="failure")
                    except:
                        return render_template('UploadAdminPhoto1.html', result="duplicate")
                else:
                    return redirect(url_for('adminphoto'))
            else:
                return render_template('UploadAdminPhoto.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='admin':
            photo = check_photo(email)
            cur = create_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/images/" + photo)
                return render_template('ChangeAdminPhoto.html', data="success")
            else:
                return render_template('ChangeAdminPhoto.html', data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medicalphoto')
def medicalphoto():
    return render_template('UploadMedicalPhoto.html')

@app.route('/medicalphoto1',methods=['GET','POST'])
def medicalphoto1():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='medical':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('UploadMedicalPhoto1.html', result="success")
                        else:
                            return render_template('UploadMedicalPhoto1.html', result="failure")
                    except:
                        return render_template('UploadMedicalPhoto1.html', result="duplicate")
                else:
                    return redirect(url_for('medicalphoto'))
            else:
                return render_template('UploadMedicalPhoto.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/change_medicalphoto')
def change_medicalphoto():
    if 'usertype' in session:
        ut=session['usertype']
        email = session['email']
        if ut == 'medical':
            photo = check_photo(email)
            cur = create_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/images/" + photo)
                return render_template('ChangeMedicalPhoto.html', data="success")
            else:
                return render_template('ChangeMedicalPhoto.html', data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))




if __name__ == '__main__':
    app.run(debug=True)