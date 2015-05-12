# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import MySQLdb
pwd = "scuderia800"

def login(request):
    check = check_login()
    if check == 1:
        return HttpResponseRedirect("/buy")
    message = ""
    name = ""
    if request.POST:
        db = MySQLdb.connect("localhost","root",pwd,"canteen" )
        cursor = db.cursor()
        cursor.execute("select * from login")
        data = cursor.fetchall()
        db.close()
        for each in data:
            if each[0]==request.POST['id']:
                if each[1]==request.POST['pwd']:
                    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
                    cursor = db.cursor()
                    cursor.execute("update login set logged_in = 1")
                    db.commit()
                    db.close()
                    return HttpResponseRedirect("/buy")
        message = "Enter Again..."  
        name = request.POST['id']
    return render(request,'login/login_page.html',{"message":message, "name":name})

def check_login():
    db = MySQLdb.connect("localhost","root",pwd,"canteen" )
    cursor = db.cursor()
    cursor.execute("select * from login")
    data = cursor.fetchall()
    db.close()
    if int(data[0][2]) == 1:
        return 1
    else:
        return 0
