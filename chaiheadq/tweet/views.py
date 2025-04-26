from django.shortcuts import render, redirect

# Create your views here.
from .models import Tweet
from .forms import TweetForm, UserRegisterationForm
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'layout.html')

def index(request):
    return render(request,'tweet/index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet/tweet_list.html',{
        'tweets':tweets
    })

@login_required
def tweet_create(request):
    form = None
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
        return render(request,'tweet/tweet_form.html',{
            'form':form
        })

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,
                               user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES,
                         instance=tweet)
        if form.is_valid():
            tweet = form.save(commit= False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
        return render(request,'tweet/tweet_form.html',{
            'form':form
        })

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk = tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    else:
        return render(request,'tweet/tweet_confirm_delete.html',{
            'tweet':tweet
        })
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegisterationForm()
    return render(request, 'registration/register.html',{
        'form':form
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tweet_list')  # or wherever you want
        else:
            # Authentication failed
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'registration/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'registration/logout.html')  # or wherever you want