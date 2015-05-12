# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import MySQLdb
import datetime
import pdb
pwd = "scuderia800"

def buy(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/login")
  
    # fetch dues data
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    sql = "select s.name,a.amount from account as a join student as s where a.roll_no = s.roll_no and a.amount < 0 order by a.amount limit 10;"
    cursor.execute(sql)
    dues_data = cursor.fetchall()
    db.close()
 
    # fetch transaction data (last 20)
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    sql = "select s.name, p.amount, p.type from student as s join purchase as p where p.roll_no=s.roll_no order by p.id desc limit 20;"
    cursor.execute(sql)
    trans_data = cursor.fetchall()
    db.close()

    # fetch total dues data
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    sql = "select sum(amount) from account where amount < 0;"
    cursor.execute(sql)
    dues = int(cursor.fetchall()[0][0])
    db.close()

    # What does this do?
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    sql = "select * from login"
    cursor.execute(sql)
    data = cursor.fetchall()
    message = ""
    name = ""
    amount = 0 

    if request.POST:
        # check if amount is valid
        try:
            eval(request.POST['amount'])
        except:
            return render(request,'buy/buy_page.html',{'negative_message':"Please enter a valid amount!", 'name':name, 'amount':amount, "roll_no":request.POST['roll_no'], 'trans_data':trans_data, 'dues':dues, 'dues_data':dues_data})
  

        if request.POST['amount'] == "":
            return render(request,'buy/buy_page.html',{'negative_message':"Please enter a value in the amount field", 'name':name, 'amount':amount,"roll_no":request.POST['roll_no'], 'trans_data':trans_data, 'dues':dues, 'dues_data':dues_data})  
        if int(eval(request.POST['amount'])) < 0:
            return render(request,'buy/buy_page.html',{'negative_message':"You cannot enter a negative value in the amount field", 'name':name, 'amount':amount,"roll_no":request.POST['roll_no'], 'trans_data':trans_data, 'dues':dues, 'dues_data':dues_data})
        db = MySQLdb.connect("localhost","root",pwd,"canteen" )
        cursor = db.cursor()
        try:
            sql = "update account set amount=amount-%d where roll_no='%s'" %(int(eval(request.POST['amount'])),request.POST['roll_no'])
            cursor.execute(sql)
            db.commit()
            db.close()
            
            #fetch new amount
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            cursor.execute("select * from account where roll_no = '%s'"%request.POST['roll_no'])
            data = cursor.fetchall()
            amount = data[0][1]
            db.close()
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            cursor.execute("select * from student where roll_no = '%s'"%request.POST['roll_no'])
            data = cursor.fetchall()
            name = data[0][1]

            #time stamp
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            purchase_amount = int(eval(request.POST['amount'])) * -1
            sql = "insert into purchase (roll_no, amount, time, type) values ('%s',%d,'%s','%s')"%(request.POST['roll_no'], purchase_amount, str(datetime.datetime.now())[0:16],"Purchase")
            cursor.execute(sql)
            db.commit()
            db.close()

            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            sql = "select s.name, p.amount, p.type from student as s join purchase as p where p.roll_no=s.roll_no order by p.id desc limit 20;"
            cursor.execute(sql)
            trans_data = cursor.fetchall()
            db.close()

            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            sql = "select sum(amount) from account where amount < 0;"
            cursor.execute(sql)
            dues = int(cursor.fetchall()[0][0])
            db.close()
        
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            sql = "select s.name,a.amount from account as a join student as s where a.roll_no = s.roll_no and a.amount < 0 order by a.amount limit 10;"
            cursor.execute(sql)
            dues_data = cursor.fetchall()
            db.close()

        except:
            message = "Sorry! This account does not exist..."
        #db.close()
    if amount < -200:
        color = "red"
    elif amount < 0:
        color = "orange"
    else:
        color = "green"
    return render(request,'buy/buy_page.html',{'message':message, 'name':name, 'amount':amount, 'trans_data':trans_data, 'color':color, 'dues':dues, 'dues_data':dues_data})

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

