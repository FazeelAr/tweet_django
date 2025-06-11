from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def profile_view(request, username):
    
    user_obj = get_object_or_404(User, username=username)
    try:
        profile = user_obj.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user_obj)

    return render(request, 'userProfile/profile_view.html', {'profile_user': user_obj, 'profile': profile})


from .forms import ProfileForm

@login_required
def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.user != profile.user:
        return redirect('userProfile:profile_view', username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userProfile:profile_view', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'userProfile/edit_profile.html', {'form': form, 'profile': profile})
