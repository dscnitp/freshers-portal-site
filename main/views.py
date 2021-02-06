# viewsfile
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pyrebase

config={
    "apiKey": "AIzaSyA1_TbZc_DAJVAosBsBXHKVnANss0_220U",
    "authDomain": "freshers-portal.firebaseapp.com",
    "databaseURL": "https://freshers-portal.firebaseio.com",
    "projectId": "freshers-portal",
    "storageBucket": "freshers-portal.appspot.com",
    "messagingSenderId": "620782197376",
    "appId": "1:620782197376:web:f7835cc81df3aced7d2465",
    "measurementId": "G-KH43ST917G",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
session1=False

def Blogs(request):
    try:
        idToken = request.session['uid']
        session1=True
    except:
        session1=False
    import datetime
    timestamp=database.child('Blogs').shallow().get().val()
    lis_time = []
    for i in timestamp:
        lis_time.append(i)
    Descriptions = []
    Titles = []
    Types = []
    Departments = []
    images = []
    Writtenbys = []
    for i in lis_time:
        Department = database.child('Blogs').child(i).child('Department').get().val()
        Description =database.child('Blogs').child(i).child('Description').get().val()
        Title =database.child('Blogs').child(i).child('Title').get().val()
        Type =database.child('Blogs').child(i).child('Type').get().val()
        Writtenby =database.child('Blogs').child(i).child('Writtenby').get().val()
        Departments.append(Department)
        Descriptions.append(Description)
        Titles.append(Title)
        Types.append(Type)
        name = database.child('users').child(Writtenby).child('name').get().val()
        image = database.child('users').child(Writtenby).child('imgUrl').get().val()
        print(image)
        Writtenbys.append(name)
        images.append(image)
    date = []
    for i in timestamp:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis = zip(lis_time, date, Descriptions,Departments,Titles,Types,Writtenbys,images)
    return render(request,"Blogs.html",{"comb_lis":comb_lis,"session1":session1})
def search(request):
    return render(request, "search.html")
def searchusers(request):
    value = request.POST.get('search')
    title = request.POST['category']
    if value is None or title is None:
        print(value ,"Value",title)
        return render(request, "search.html")
    else:
        print(value)
        if title == "Notes":
            data = database.child('Notes').shallow().get().val()
            id = []
            for i in data:
                id.append(i)
            for i in id:
                val = database.child('Notes').child(i).child('filename').get().val()
                if (val == value):
                    requid = i
                else:
                    return render(request, "search.html")
            print(requid)
            fileurl = database.child('Notes').child(requid).child('fileurl').get().val()
            return render(request, "searchNotes.html", {"fileurl":fileurl})
        if title == "Question-papers":
            data = database.child('Question-papers').shallow().get().val()
            id = []
            for i in data:
                id.append(i)
            for i in id:
                val = database.child('Question-papers').child(i).child('filename').get().val()
                if (val== value):
                    requid = i
                else:
                    return render(request, "search.html")
            print(requid)
            fileurl = database.child('Question-papers').child(requid).child('fileurl').get().val()
            return render(request, "searchNotes.html", {"fileurl": fileurl})
        if title == "Users":
            data = database.child('users').shallow().get().val()
            uidlist = []
            requid = 'null'
            for i in data:
                uidlist.append(i)
            for i in uidlist:
                val = database.child('users').child(i).child('name').get().val()
                val=val.lower()
                value=value.lower()
                print(val,value)
                if (val == value):
                    requid = i
            if requid=='null':
                return render(request, "search.html")
            print(requid)
            name = database.child('users').child(requid).child('name').get().val()
            course = database.child('users').child(requid).child('course').get().val()
            branch = database.child('users').child(requid).child('branch').get().val()
            img = database.child('users').child(requid).child('imgUrl').get().val()
            Name = []
            Name.append(name)
            Course = []
            Course.append(course)
            Branch = []
            Branch.append(branch)
            Image = []
            Image.append(img)
            comb_lis = zip(Name, Course, Branch, Image)
            return render(request, "SearchUsers.html", {"comb_lis": comb_lis})
def searchnotes(request):
    return render(request,"searchNotes.html")
def signIn(request):
    return render(request,"Login.html")

def postsignIn(request):
    if request.method=='POST':
        email = request.POST.get('email')
        pasw = request.POST.get('pass')
        try:
            user = authe.sign_in_with_email_and_password(email, pasw)
        except:
            message = "Invalid Credentials!! Please Check your credentials and try sign-in again"
            return render(request, "Login.html", {"message": message})
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        idToken = request.session['uid']
        if idToken:
            a = authe.get_account_info(idToken)
            a = a['users']
            a = a[0]
            uid = a['localId']
            import datetime
            timestamp = database.child('Blogs').shallow().get().val()
            if timestamp:
                lis_time = []
                for i in timestamp:
                    lis_time.append(i)
                Descriptions = []
                Titles = []
                Types = []
                Departments = []
                Writtenbys = []
                for i in lis_time:
                    Department = database.child('Blogs').child(i).child('Department').get().val()
                    Description = database.child('Blogs').child(i).child('Description').get().val()
                    Title = database.child('Blogs').child(i).child('Title').get().val()
                    Type = database.child('Blogs').child(i).child('Type').get().val()
                    Writtenby = database.child('Blogs').child(i).child('Writtenby').get().val()
                    if uid == Writtenby:
                        Departments.append(Department)
                        Descriptions.append(Description)
                        Titles.append(Title)
                        Types.append(Type)
                        name = database.child('users').child(Writtenby).child('name').get().val()
                        Writtenbys.append(name)
                date = []
                for i in timestamp:
                    i = float(i)
                    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
                    date.append(dat)
                name = database.child('users').child(uid).child('name').get().val()
                branch = database.child('users').child(uid).child('branch').get().val()
                image = database.child('users').child(uid).child('imgUrl').get().val()
                if image == "":
                    image = "https://firebasestorage.googleapis.com/v0/b/freshers-portal.appspot.com/o/profilepic.jpg?alt=media&token=864cf64c-a0ad-442b-8ca2-ae425baf43ad"

                comb_lis = zip(lis_time, date, Descriptions, Departments, Titles, Types, Writtenbys)
                return render(request, "ProfilePage.html", {"comb_lis": comb_lis, "name": name, "branch": branch,"image":image})
            else:
                Descriptions = []
                Titles = []
                Types = []
                Departments = []
                date=[]
                Writtenbys = []
                lis_time=[]
                name = database.child('users').child(uid).child('name').get().val()
                branch = database.child('users').child(uid).child('branch').get().val()
                image = database.child('users').child(uid).child('imgUrl').get().val()
                print(image)
                comb_lis = zip(lis_time, date, Descriptions, Departments, Titles, Types, Writtenbys)
                return render(request, "ProfilePage.html",
                              {"comb_lis": comb_lis, "name": name, "branch": branch, "image": image})
    message = "Please Login First"
    return render(request, "Login.html", {"message": message})

def reset(request):
    return render(request, "Reset.html")

def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message  = "A link to reset your password is succesfully sent to your email"
        return render(request, "Reset.html", {"msg":message})
    except:
        message  = "Something Went Wrong, Please check the email you provided is already registered or not!!"
        return render(request, "Reset.html", {"msg":message})

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")

def signUp(request):
    return render(request,"Registration.html")

def postsignup(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        branch=request.POST.get('sel')
        enroll=request.POST.get('enrolls')
        roll=request.POST.get('roll')
        email=request.POST.get('email')
        passw=request.POST.get('pass')
        try:
            user=authe.create_user_with_email_and_password(email,passw)
        except:
            messg="Something Went Wrong, Unable to create your account. Try Again!"
            return render(request,"Registration.html",{"messg":messg})
        uid = user['localId']
        data={"name":name,"USER_TYPE":"user","device_token":"","email":email,"id":roll,"imgUrl":"https://firebasestorage.googleapis.com/v0/b/freshers-portal.appspot.com/o/profilepic.jpg?alt=media&token=864cf64c-a0ad-442b-8ca2-ae425baf43ad","branch":branch,"uid":uid,"enrollment":enroll}
        database.child("users").child(uid).set(data)
        return render(request,"Login.html")
    message = "Please Login Here First "
    return render(request, "Login.html", {"message": message})
def profile(request):
    try:
        idToken = request.session['uid']
    except:
        message = "Please Login In Here First "
        return render(request, "Login.html", {"message": message})
    if idToken:
        a = authe.get_account_info(idToken)
        a = a['users']
        a = a[0]
        uid = a['localId']
        import datetime
        timestamp = database.child('Blogs').shallow().get().val()
        lis_time = []
        for i in timestamp:
            lis_time.append(i)
        Descriptions = []
        Titles = []
        Types = []
        Departments = []
        Writtenbys = []
        for i in lis_time:
            Department = database.child('Blogs').child(i).child('Department').get().val()
            Description = database.child('Blogs').child(i).child('Description').get().val()
            Title = database.child('Blogs').child(i).child('Title').get().val()
            Type = database.child('Blogs').child(i).child('Type').get().val()
            Writtenby = database.child('Blogs').child(i).child('Writtenby').get().val()

            if uid == Writtenby:
                Departments.append(Department)
                Descriptions.append(Description)
                Titles.append(Title)
                Types.append(Type)
                name = database.child('users').child(Writtenby).child('name').get().val()
                branch = database.child('users').child(Writtenby).child('branch').get().val()
                Writtenbys.append(name)
        date = []
        for i in timestamp:
            i = float(i)
            dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
            date.append(dat)
        name = database.child('users').child(uid).child('name').get().val()
        branch = database.child('users').child(uid).child('branch').get().val()
        image = database.child('users').child(uid).child('imgUrl').get().val()
        if image=="":
            image="https://firebasestorage.googleapis.com/v0/b/freshers-portal.appspot.com/o/profilepic.jpg?alt=media&token=864cf64c-a0ad-442b-8ca2-ae425baf43ad"
        comb_lis = zip(lis_time, date, Descriptions, Departments, Titles, Types, Writtenbys)
        return render(request,"ProfilePage.html",{"comb_lis":comb_lis,"name":name,"branch":branch,"image":image})

def addPost(request):
        return render(request,"AddPost.html")
def about(request):
    try:
        idToken = request.session['uid']
        session1=True
    except:
        session1=False
    return render(request, "aboutcollege.html",{"session1":session1})
def home(request):
    try:
        idToken = request.session['uid']
        session1=True
    except:
        session1=False
    return render(request, "home2.html",{"session1":session1})
def afteraAddPost(request):
    if request.method=='POST':
        from datetime import datetime, timezone
        import time
        import pytz
        idToken = request.session['uid']
        if idToken:
            tz = pytz.timezone('Asia/Kolkata')
            Currenttime = datetime.now(timezone.utc).astimezone(tz).strftime("%H%M%S")
            millis = int(Currenttime)
            tyype = request.POST.get('type')
            title = request.POST.get('title')
            description = request.POST.get('desc')
            branch=request.POST.get('sel')
            a = authe.get_account_info(idToken)
            a = a['users']
            a = a[0]
            a = a['localId']

            data ={
                "Type":tyype,
                "Title":title,
                "Description":description,
                "Writtenby":a,
                "Time":Currenttime,
                "Department":branch,
            }
            database.child('Blogs').child(millis).set(data)
            import datetime
            a = authe.get_account_info(idToken)
            a = a['users']
            a = a[0]
            a = a['localId']
            timestamp = database.child('Blogs').shallow().get().val()
            lis_time = []
            for i in timestamp:
                lis_time.append(i)
            Descriptions = []
            Titles = []
            Types = []
            Departments = []
            Writtenbys = []
            for i in lis_time:
                Department = database.child('Blogs').child(i).child('Department').get().val()
                Description = database.child('Blogs').child(i).child('Description').get().val()
                Title = database.child('Blogs').child(i).child('Title').get().val()
                Type = database.child('Blogs').child(i).child('Type').get().val()
                Writtenby = database.child('Blogs').child(i).child('Writtenby').get().val()
                if a == Writtenby:
                    Departments.append(Department)
                    Descriptions.append(Description)
                    Titles.append(Title)
                    Types.append(Type)
                    name = database.child('users').child(Writtenby).child('name').get().val()
                    branch = database.child('users').child(Writtenby).child('branch').get().val()
                    Writtenbys.append(name)
            date = []
            for i in timestamp:
                i = float(i)
                dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
                date.append(dat)
            comb_lis = zip(lis_time, date, Descriptions, Departments, Titles, Types, Writtenbys)
            image = database.child('users').child(a).child('imgUrl').get().val()
            return render(request, "ProfilePage.html", {"comb_lis": comb_lis,"name":name,"branch": branch,"image":image})
    message = "Please Login First"
    return render(request, "Login.html", {"message": message})

def gotoedit(request):
    idToken = request.session['uid']
    if idToken:
        a = authe.get_account_info(idToken)
        a = a['users']
        a = a[0]
        uid = a['localId']

    image = database.child('users').child(uid).child('imgUrl').get().val()
    name = database.child('users').child(uid).child('name').get().val()
    branch = database.child('users').child(uid).child('branch').get().val()
    enrollment = database.child('users').child(uid).child('enrollment').get().val()
    if image == "":
        image = "https://firebasestorage.googleapis.com/v0/b/freshers-portal.appspot.com/o/profilepic.jpg?alt=media&token=864cf64c-a0ad-442b-8ca2-ae425baf43ad"
    return render(request,'editprofile.html',{"image":image,"name":name,"branch":branch,"enrollment":enrollment})

def postedit(request):
    if request.method=='POST':
        import time
        from datetime import datetime,timezone
        import pytz
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))

        imgurl=request.POST.get('url')        #for image update
        print("IMAGEurl",imgurl)

        idtoken=request.session['uid']
        a = authe.get_account_info(idtoken)
        a=a['users']
        a=a[0]
        a=a['localId']
        data={                              #image update remaining--sumit
            "imgUrl":imgurl,
        }
        database.child('users').child(a).update(data)
        return render(request,'home2.html')
    message = "Please Login First"
    return render(request, "Login.html", {"message": message})
