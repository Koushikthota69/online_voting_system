from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Election, Candidate, Vote
from .forms import VoteForm, RegisterForm
from .forms import UserProfileForm



def home(request):
    return render(request, 'voting/home.html')

def list_elections(request):
    elections = Election.objects.all()
    return render(request, 'voting/list_elections.html', {'elections': elections})

@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Ensure the user has a valid college_id
    if not user_profile.college_id:
        messages.error(request, "Your profile is incomplete. Please update your college ID.")
        return redirect('update_profile')  # Assuming you have an update profile view

    # Check if the user has already voted
    if Vote.objects.filter(election=election, voter=request.user).exists():
        messages.error(request, "You have already voted in this election!")
        return redirect('list_elections')

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            # Check if the submitted college_id matches the one in the user profile
            input_college_id = form.cleaned_data.get("college_id")
            if input_college_id != user_profile.college_id:
                messages.error(request, "voter_id is not valid")
                return redirect('vote', election_id=election.id)
            vote = form.save(commit=False)
            vote.voter = request.user
            vote.election = election
            vote.college_id = user_profile.college_id  # Use the validated college_id
            vote.save()
            messages.success(request, "Vote cast successfully!")
            return redirect('results', election_id=election.id)
    else:
        # Pre-populate the form with the user's college_id
        form = VoteForm(initial={'college_id': user_profile.college_id})

    return render(request, 'voting/vote.html', {
        'election': election,
        'candidates': candidates,
        'form': form
    })

def results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    votes = Vote.objects.filter(election=election)
    return render(request, 'voting/results.html', {'election': election, 'votes': votes})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    return render(request, 'voting/login.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "voting/register.html", {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

@login_required
def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    if request.user.is_superuser:
        election.delete()
        messages.success(request, "Election deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this election.")
    return redirect('list_elections')
@login_required
def update_profile(request):
    profile = request.user.userprofile
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'voting/update_profile.html', {'form': form})