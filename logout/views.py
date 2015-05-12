# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import MySQLdb

def logout(request):
    db = MySQLdb.connect("localhost","root","scuderia800","canteen" )
    cursor = db.cursor()
    sql = "update login set logged_in = 0"
    cursor.execute(sql)
    db.commit()
    db.close()   
    return HttpResponseRedirect("/login")
