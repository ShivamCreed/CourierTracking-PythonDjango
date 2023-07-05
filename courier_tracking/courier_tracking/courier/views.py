from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from .models import *
import datetime

def index(request):
    return render(request,'index.html')

def login(request):
    error=""
    if request.method == "POST":
        ur = request.POST['uname']
        pd = request.POST['pwd']
        user = auth.authenticate(username=ur,password=pd)
        try:
            if user.is_staff:
                auth.login(request,user)
                error = "no"
            elif user is not None:
                auth.login(request,user)
                return redirect('user_home')
                error = "not"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error':error}
    return render(request,'login.html',d)

def signup(request):
    error = ""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        p = request.POST['pwd']
        gen = request.POST['gender']
        i=request.FILES['image']
        addr=request.POST['address']
        d=request.POST['dob']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            Signup.objects.create(user=user,mobile=con,image=i,gender=gen,address=addr,dob=d)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'signup.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'admin_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Signup.objects.all()
    d = {'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordadmin.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'user_home.html')

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passworduser.html',d)

def feedback(request):
    if not request.user.is_authenticated:
        return redirect('feedback')
    error=""
    if request.method=='POST':
        n = request.POST['fname']
        p = request.POST['fphone']
        e = request.POST['femail']
        c = request.POST['fcomment']
        try:
            Feedback.objects.create(feedback_name=n,feedback_contact=p,feedback_email=e,feedback_comment=c)
            error = "no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'feedback.html',d)

def view_feedback(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Feedback.objects.all()
    d = {'data':data}
    return render(request,'view_feedback.html',d)

def delete_feedback(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    feedback = Feedback.objects.get(id=id)
    feedback.delete()
    return redirect('view_feedback')

def send_parcel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    time = datetime.datetime.today()
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        c=request.POST['contact']
        pt=request.POST['ptype']
        rd=request.POST['rdate']
        gi=request.POST['gid']
        gn=request.POST['gidn']
        w=request.POST['weight']
        add=request.POST['address']
        try:
            ParcelRequest.objects.create(first_name=f,last_name=l,email=e,mobile=c,parcel_type=pt,request_date=rd,gov_id=gi,gov_no=gn,weight=w,address=add,status="Pending")
            error="no"
        except:
            error="yes"
    d={'time':time,'user':user,'error':error}
    return render(request,'send_parcel.html',d)

def view_my_parcel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = ParcelRequest.objects.all()

    d={'data':data}
    return render(request,'view_my_parcel.html',d)

def view_parcel_admin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = ParcelRequest.objects.all()
    data2 = Receiver.objects.all()
    d={'data':data,'data2':data2}
    return render(request,'view_parcel_admin.html',d)

def change_status(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking=ParcelRequest.objects.get(id=id)
    error=""
    if request.method == "POST":
        rs = request.POST['rstatus']
        booking.status = rs
        try:
            booking.save()
            error = "no"
        except:
            error = "yes"
    d = {'booking': booking,'error':error}
    return render(request,'change_status.html',d)

def delete_parcel(request,id):
    data=ParcelRequest.objects.get(id=id)
    data.delete()
    return redirect('view_my_parcel')

def sender_detail(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    pr = ParcelRequest.objects.get(id=id)
    w= int(pr.weight)*100
    time = datetime.datetime.today()
    error=""
    if request.method=='POST':
        n=request.POST['fname']
        c=request.POST['contact']
        pin=request.POST['pin_code']
        hou=request.POST['house']
        city=request.POST['city']
        st=request.POST['state']
        sd=request.POST['send_date']
        pid=444+int(id)
        try:
            Receiver.objects.create(name=n,contact=c,pin=pin,house=hou,
                                    city=city,state=st,send_date=sd,parcel_id=pid,
                                    parcel_status="Your Parcel is Shipped")
            pr.parcel_id=pid
            pr.save()
            error="no"
        except:
            error="yes"
    d={'time':time,'w':w,'error':error}
    return render(request,'sender_detail.html',d)

def check_status_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Receiver.objects.get(parcel_id=pid)
    d={'data':data}
    return render(request,'check_status_user.html',d)


def change_track_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    time=datetime.datetime.today()
    data = Receiver.objects.get(parcel_id=pid)
    if request.method=="POST":
        sv=request.POST['status_value']
        dt=request.POST['date_time']
        msg=request.POST['message']
        try:
            data.parcel_status=sv
            data.parcel_date=dt
            data.parcel_msg=msg
            data.save()
            error="no"
        except:
            error="yes"
    d={'data':data,'time':time,'error':error}
    return render(request,'change_track_status.html',d)

def visitor_track(request):
    error="yes"
    try:
        if request.method=='POST':
            vid=request.POST['vid']
            vid=int(vid)
            data = Receiver.objects.all()
            d={'vid':vid,'data':data}
            return render(request,'parsel_location.html',d)
    except:
        error="no"
    d={'error':error}
    return render(request,'visitor_track.html',d)

def parsel_location(request):
    data=Receiver.objects.all()
    d={'data':data}
    return render(request,'parsel_location.html',d)

