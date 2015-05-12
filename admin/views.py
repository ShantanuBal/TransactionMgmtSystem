# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import MySQLdb
import datetime
import pdb
pwd = "scuderia800"
secret_key = "lucky24"

def admin(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/login")
    
    sum = 0
    data = ""
    if request.POST:
        if request.POST['sk'] == secret_key:            
            db = MySQLdb.connect("localhost","root",pwd,"canteen" )
            cursor = db.cursor()
            sql = "select s.name, a.amount from account as a join student as s where a.roll_no = s.roll_no order by s.name;"
            cursor.execute(sql)
            data = cursor.fetchall()
            db.close()
            sum = 0
            for each in data:
                sum += each[1]
    return render(request,'admin/admin2.html',{'data':data, 'sum':sum})

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
