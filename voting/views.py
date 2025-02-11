from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Election, Candidate, Vote
from .forms import VoteForm, RegisterForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'voting/home.html')

def list_elections(request):
    elections = Election.objects.all()
    return render(request, 'voting/list_elections.html', {'elections': elections})

@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            college_id = form.cleaned_data['college_id']
            if Vote.objects.filter(election=election, college_id=college_id).exists():
                return render(request, 'voting/vote.html', {'error': "You have already voted!", 'election': election, 'candidates': candidates})
            
            vote = form.save(commit=False)
            vote.voter = request.user
            vote.election = election
            vote.save()
            return redirect('results', election_id=election.id)

    else:
        form = VoteForm()
    
    return render(request, 'voting/vote.html', {'election': election, 'candidates': candidates, 'form': form})

def results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    votes = Vote.objects.filter(election=election)
    return render(request, 'voting/results.html', {'election': election, 'votes': votes})

def login_view(request):
    return render(request, 'voting/login.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = RegisterForm()

    return render(request, 'voting/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

