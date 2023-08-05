from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import BlogPost, Comment
from math import ceil
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


count = 0
def blogHome(request):
    global count

    blogs = BlogPost.objects.all()
    views = [[item.views, item.blog_id] for item in blogs]

    views.sort()
    views = views[-1:-6:-1]
    l=[views[i][1] for i in range(len(views))]

    l1=[]
    for i in l:
        obj = BlogPost.objects.filter(blog_id=i).first()
        l1.append(obj)

    msg = False
    if request.user.is_authenticated:
        msg = request.user.first_name
        count+=1

    parameters = {'blogs': l1, "number": blogs, "msg": msg, "count": count}
    return render(request, 'blog/blogHome.html', parameters)


def messenger(request):
    messages.info(request, 'This feature would be available in upcoming updates!')
    return redirect('/blog')


def search(request):
    blogs = BlogPost.objects.all()

    query = request.GET.get('search', '')
    if query == '':
        l=[]
    else:
        l = query.split(' ')

    count=0
    for i in l:
        if i == '':
            count+=1
    if count == len(l):
        l=[]


    if len(l)==0:
        views = [[item.views, item.blog_id] for item in blogs]
        views.sort()
        views = views[-1:-6:-1]
        x=[views[i][1] for i in range(len(views))]

        l1=[]
        for i in x:
            obj = BlogPost.objects.filter(blog_id=i).first()
            l1.append(obj)

        parameters = {'blogs': l1, "number": blogs}
        return render(request, 'blog/blogHome.html', parameters)



    blog = [i for i in blogs if searchMatch(l, i)]

    if len(l)>12:
        messages.warning(request, "Too long query entered, search ignored!")
    elif len(blog)==0:
        messages.warning(request, "Please try searching a valid query!")

    parameters = {'blogs': blog, 'query': query}
    return render(request, 'blog/search.html', parameters)


def searchMatch(query, item):
    matched = 0
    length=len(query)

    for words in query:
        words = words.lower()
        # words = f'{words} '
        if words in item.title.lower() or words in item.category.lower() or words in item.heading01.lower() or words in item.heading02.lower() or words in item.heading03.lower() or words in item.content01.lower() or words in item.content02.lower() or words in item.content03.lower():
            matched+=1

    for i in range(1, 13):
        if length==i:
            if matched>i-1:
                return True
    return False


def index(request):
    blogs = BlogPost.objects.all()
    parameters = {'blogs': blogs}
    return render(request, 'blog/index.html', parameters)
 

def blogPost(request, blg_id):
    blogs = BlogPost.objects.all()

    posts = BlogPost.objects.filter(blog_id=blg_id).first()
    posts.views+=1
    posts.save()
    comments = Comment.objects.filter(post=posts, parent=None)
    replies = Comment.objects.filter(post=posts).exclude(parent=None)

    reply_count = []
    for i in comments:
        temp=0
        for j in replies:
            if j.parent.s_no == i.s_no:
                temp+=1
        reply_count.append([i, temp])
    
    l=[]
    for i in blogs:
        l.append(i.blog_id)

    return render(request, 'blog/blogPost.html', {'post': posts, 'len': len(blogs), 'ids': l, "comments": reply_count, "replies":replies})


def blogComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_sno = request.POST.get('post_sno')
        post = BlogPost.objects.get(blog_id=post_sno)
        parentsno = request.POST.get('parent_sno')

        if parentsno == "":
            cmt = Comment(your_comment=comment, user=user, post=post)
            cmt.save()
            messages.success(request, "Comment posted successfully!")

        else:
            parent = Comment.objects.get(s_no=parentsno)
            cmt = Comment(your_comment=comment, user=user, post=post, parent=parent)
            cmt.save()
            messages.success(request, "Reply posted successfully!")
      
    return redirect(f'/blog/BlogPost/{post_sno}')



def addPost(request):
    if request.method=='POST':
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        intro = request.POST.get('intro', '')
        h1 = request.POST.get('h1', '')
        c1 = request.POST.get('c1', '')
        h2 = request.POST.get('h2', '')
        c2 = request.POST.get('c2', '')
        h3 = request.POST.get('h3', '')
        c3 = request.POST.get('c3', '')
        image = request.POST.get('img', '')

        new_added_post = BlogPost(category=category, title=title, intro=intro, heading01=h1, content01=c1, heading02=h2, content02=c2, heading03=h3, content03=c3, image=image)
        new_added_post.save()

        goimage(image)

        Id = new_added_post.blog_id
        check = 'a'
        messages.success(request, "Post added successfully!")
        # return render(request, 'blog/addPost.html', {'new_id': Id, 'check': check})
        return redirect(f'/blog/BlogPost/{Id}')

    return render(request, 'blog/addPost.html')

def customPost(request):
    if request.method=='POST':
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        intro = request.POST.get('intro', '')
        content = request.POST.get('whole-content', '')
        image = request.POST.get('img')

        new_added_post = BlogPost(category=category, title=title, intro=intro, whole_content=content, image=image)
        new_added_post.save()

        goimage(image)

        Id = new_added_post.blog_id
        check = 'a'
        messages.success(request, "Post added successfully!")
        # return render(request, 'blog/customPost.html', {'new_id': Id, 'check': check})
        return redirect(f'/blog/BlogPost/{Id}')

    return render(request, 'blog/customPost.html')


# Authentication APIs below----
def handleLogin(request):
    if request.method=='POST':
        username = request.POST.get('login_username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f"successfully logged in as {username}")
            return redirect('/blog')

        else:
            messages.error(request, "Invalid username or password...")
            return redirect('/blog')
    else:
        return render(request, 'blog/notfound.html')

def Logout(request):
    global count

    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged out!")

        count = 0
        return redirect('/blog')
    else:
        messages.info(request, "No user has logged in yet")
        return redirect('/blog')


def handleSing_up(request):
    global count

    if request.method=='POST':
        username = request.POST.get('username', '')
        username = username.lower()
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')
        check = request.POST.get('check', '')

        # check errors here
        if pass1!=pass2:
            messages.warning(request, "Your entered passwords did not match each other. Please try again...")
            return redirect('/blog')

        if username[0].isdigit() or username[0] == ' ':
            messages.info(request, "Usernamae must not start with a digit or a space.")
            return redirect('/blog')


        not_allowed = '''+!@#$%&*^~][}{`',<>|\/:;=?"'''
        for i in not_allowed:
            if i in username:
                messages.info(request, '''Usernamae cannot contain +!@#$%&*^~][}{`',<>|\/:;=?" characters''')

                return redirect('/blog')


        # adding user
        try:
            user = User.objects.create_user(username, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            
            if check == 'remember-me':
                user = authenticate(username = username, password = pass1)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Account successfully created!")
                    messages.success(request, f"successfully logged in as {username}!")

                    count = -100000
                    return redirect('/blog')

            else:
                messages.success(request, "Account successfully created!")
                count = -100000
                return redirect('/blog')

        except Exception as e:
            messages.error(request, "This username already exists. Please Try entering a unique username!")
            return redirect('/blog')
    
    else:
        return render(request, 'blog/notfound.html')




# Taking image to the required path
import os
import shutil

def goimage(image):
    initial_path =''
    for (root,dirs,files) in os.walk('D:\\', topdown=True):
        # print (root)
        # print (dirs)
        # print(files)

        for file in files:
            if file == image:
                initial_path = f'{root}\{file}'
    shutil.copyfile(initial_path, f'D:\django projects\E-Commerce\webcart\media\{image}')


    