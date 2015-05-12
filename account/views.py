# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import MySQLdb
import datetime
import pdb
pwd = "scuderia800"
secret_key = "lucky24"

def create_account(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/login")


    message = ""
    if request.POST:   
        # check if amount is valid
        try:
            eval(request.POST['advance'])
        except:
            return render(request,'account/create_account.html',{'message':"Invalid amount entered. Please try again!"})

        if request.POST['key'] != secret_key:
            return render(request,'account/create_account.html',{'message':"Invalid secret key..."})
        try:
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            sql = "insert into student values ('%s','%s','%s')"%(request.POST['roll_no'], request.POST['name'], request.POST['email'])
            cursor.execute(sql)
            sql = "insert into account values ('%s',%d)"%(request.POST['roll_no'],int(request.POST['advance']))
            cursor.execute(sql)
            db.commit()
            db.close()
            message = "Hi %s, your account has been created! You may now use it for your purchase. Thanks!"%request.POST['name']
            
            #time stamp
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            insert_amount = int(request.POST['advance']) 
            sql = "insert into purchase (roll_no, amount, time, type) values ('%s',%d,'%s','%s')"%(request.POST['roll_no'], insert_amount, str(datetime.datetime.now())[0:16],"Account Opening")
            cursor.execute(sql)
            db.commit()
            db.close()
        except:
            message="This account already exists..."
    return render(request,'account/create_account.html',{'message':message})

def top_up_account(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/login")
    message = ""
    name = ""
    amount = ""
    if request.POST:
        if request.POST['key'] != secret_key :
            return render(request,'account/top_up_account.html',{'message':"Incorrect secret key...", 'name':name, 'amount':amount, "roll_no":request.POST["roll_no"],"top_up_amount":request.POST['amount']})
        db = MySQLdb.connect("localhost","root",pwd,"canteen" )
        cursor = db.cursor()
        cursor.execute("select * from account where roll_no='%s'"%request.POST['roll_no'])
        data = cursor.fetchall()
        db.close()
        if data:
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor() 
            cursor.execute("update account set amount=%d where roll_no='%s'"%(int(request.POST['amount'])+int(data[0][1]),request.POST['roll_no']))
            db.commit()
            db.close()
            amount = int(data[0][1])+int(request.POST['amount'])
            #fetch name
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            cursor.execute("select * from student where roll_no='%s'"%request.POST['roll_no'])
            data = cursor.fetchall()
            name = data[0][1]
            db.close()
            #time stamp
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            insert_amount = int(request.POST['amount'])
            sql = "insert into purchase (roll_no, amount, time, type) values ('%s',%d,'%s','%s')"%(request.POST['roll_no'], insert_amount, str(datetime.datetime.now())[0:16],"Top up")
            cursor.execute(sql)
            db.commit()
            db.close()

        else:            
            message = "Roll number not found in our records. Please enter again or create an account."
    # assign color
    if amount < -200:
        color = "red"
    elif amount < 0:
        color = "orange"
    else:
        color = "green"

    return render(request,'account/top_up_account.html',{'message':message, 'name':name, 'amount':amount, 'color':color})

def view_account(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/login")
    message = ""
    amount = ""
    name = ""
    timestamp_data = ""
    if request.POST:
        db = MySQLdb.connect("localhost","root",pwd,"canteen" )
        cursor = db.cursor()
        cursor.execute("select * from account where roll_no='%s'"% request.POST['roll_no'])
        data = cursor.fetchall()
        db.close()
        print data
        for each in data:
            if each[0]==request.POST['roll_no']:
                    amount = each[1]
                    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
                    cursor = db.cursor()
                    cursor.execute("select * from student where roll_no='%s'"%request.POST['roll_no'])
                    data = cursor.fetchall()
                    name = data[0][1]
                    db.close()
                    #fetch timestamps
                    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
                    cursor = db.cursor()
                    cursor.execute("select amount,type,time from purchase where roll_no='%s'"%request.POST['roll_no'])
                    timestamp_data = cursor.fetchall()    
                    timestamp_data                
                    db.close()
                    break
        else:
            message = "Roll number not found in our records. Please enter again or create an account."
    # assign color
    if amount < -200:
        color = "red"
    elif amount < 0:
        color = "orange"
    else:
        color = "green"

    return render(request,'account/view_account.html',{'color':color, 'amount':amount,'message':message, 'name':name, 'timestamp_data':timestamp_data})

def change_pin(request):
    message = ""
    name = ""
    if request.POST:
        if request.POST['pin'] == "":
            return render(request,'account/change_pin.html',{'message':"Please enter the original PIN and try again!"})
        if request.POST['new_pin1'] != request.POST['new_pin2']:
            return render(request,'account/change_pin.html',{'message':"PIN mismatch...enter the new PIN again!"})
        
        #check if new pin alread exists
        db = MySQLdb.connect("localhost","root",pwd,"canteen")
        cursor = db.cursor()
        cursor.execute("select * from account where roll_no='%s'"% request.POST['new_pin1'])
        data = cursor.fetchall()
        db.close()
        if data:
            return render(request,'account/change_pin.html',{'message':"New PIN is already taken...please select another PIN!"})
       
        #check if old pin is present in DB
        db = MySQLdb.connect("localhost","root",pwd,"canteen")
        cursor = db.cursor()
        cursor.execute("select * from account where roll_no='%s'"% request.POST['pin'])
        data = cursor.fetchall()
        db.close()
        if data:
            
            db = MySQLdb.connect("localhost","root",pwd,"canteen")
            cursor = db.cursor()
            cursor.execute("update account set roll_no='%s' where roll_no='%s'"% (request.POST['new_pin1'], request.POST['pin']))
            db.commit()
            cursor.execute("update student set roll_no='%s' where roll_no='%s'"% (request.POST['new_pin1'], request.POST['pin']))
            db.commit()
            cursor.execute("update purchase set roll_no='%s' where roll_no='%s'"% (request.POST['new_pin1'], request.POST['pin']))
            db.commit()
            db.close()
            message = "Your PIN has been changed successfully!"
            # fetch name
            db = MySQLdb.connect("localhost","root",pwd,"canteen")
            cursor = db.cursor()
            cursor.execute("select name from student where roll_no='%s'"% request.POST['new_pin1'])
            data = cursor.fetchall()
            db.close()
            name = data[0][0]
        else:
            message = "Original PIN not found in our records...please enter again!"
    return render(request,'account/change_pin.html',{'message':message, 'name':name})

def check_login():
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    cursor.execute("select * from login")
    data = cursor.fetchall()
    db.close()
    if data[0][2] == 0:
        return 1
    else:
        return 0

