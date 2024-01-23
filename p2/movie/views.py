from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def movie(request):
    if request.method == "POST":

        data=request.POST
        movie_img=request.FILES.get('movie_img')
        movie_name=data.get('movie_name')
        movie_desc=data.get('movie_desc')
    #    ab db ma data save krna hy
        Movie.objects.create(
        movie_img=movie_img,
        movie_name=movie_name,
        movie_desc=movie_desc
        )
        return redirect('/movie/')
    # queryset=Movie.objects.all()
    # context={'movie':queryset}
    return render(request,'movie.html')
@login_required(login_url="/login/")
def movie_list(request):
    queryset=Movie.objects.all()
    
    if request.GET.get('search'):
        queryset=Movie.objects.filter(movie_name__icontains=request.GET.get('search'))


    
    
    return render(request,'show.html',context={'movie':queryset})
@login_required(login_url="/login/")
def delete_movie(request,id):
    queryset=Movie.objects.get(id = id)
    queryset.delete()
    return redirect("/movie-list/")
@login_required(login_url="/login/")
def update_movie(request,id):
    queryset=Movie.objects.get(id= id)
    if request.method=="POST":
        data=request.POST
        movie_name=data.get('movie_name')
        movie_desc=data.get('movie_desc')
        movie_img=request.FILES.get('movie_img')

        queryset.movie_name=movie_name
        queryset.movie_desc=movie_desc
        if movie_img:
            queryset.movie_img=movie_img
        queryset.save()
        return redirect('/movie-list/')
    context={'movie':queryset}
    return render(request,'update_movie.html',context)

# def login_page(request):
#     # if request.method=="POST":
#     #     data=request.POST
#     #     username=data.get(username),
#     #     password=data.get(password)
    
#     return render(request,'login_page.html')
def register_page(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        username=data.get('username'),
        password=data.get('password')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "This username is already exists.")
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Your account is created.")

        return redirect('/register/')
    return render(request,'register.html')
def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username'),
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if not user.exists():
            messages.info(request, "username is not valid.")
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request, "password is not correct.")
        else:
            login(request,user)
            return redirect('/movie-list/')

    return render(request,'login_page.html')
@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect('/login/')