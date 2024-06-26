from django.shortcuts import render , redirect
from .forms import RegistrationForm , PostForm
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group , User
from .models import Post

# Create your views here.


@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        user_id = request.POST.get("user_id")
        if post_id:
            post = Post.objects.get(id= post_id)
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.get(id = user_id)
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name="default")
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name="mod")
                    group.user_set.remove(user)
                except:
                    pass

    return render(request,'main/home.html',{"posts":posts})

@login_required(login_url='/login')
@permission_required('main.add_post' ,login_url="/login" , raise_exception=True)
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()
    return render(request, "main/post_create.html" , {"form" : form})




def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user)
            return redirect('/login')

    
    else:
        form = RegistrationForm()

    
    return render(request, "registration/sign_up.html" , {"form":form})
