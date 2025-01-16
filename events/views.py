from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tournament, Team, Player,PlayerRegistration

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tournament_dashboard')  # Redirect to the tournament dashboard page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        game = request.POST['game']
        weight = request.POST['weight']
        category = request.POST['category']

        # Create a new player instance and save it to the database
        player = Player.objects.create(
            username=username,
            password=password,
            name=name,
            email=email,
            age=age,
            game=game,
            weight=weight,
            category=category
        )
        player.save()

        # Login the player
        login(request, player)
        return redirect('tournament_dashboard')
    else:
        print("an error occurd")
    return render(request, 'login.html')

@login_required
def player_profile(request):
    try:
        player = request.user.player
    except Player.DoesNotExist:
        messages.error(request, 'You do not have a player profile. Please register as a player.')
        return redirect('register')
    return render(request, 'player_profile.html', {'player': player})

def tournament_dashboard(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_dashboard.html', {'tournaments': tournaments})

def team_profile(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        messages.error(request, 'Team not found.')
        return redirect('tournament_dashboard')
    return render(request, 'team_profile.html', {'team': team})

def logout_view(request):
    logout(request)
    return redirect('login')

def contact_us(request):
    return render(request, 'contact_us.html')

def info(request):
    return render(request, 'info.html')

def fixtures(request):
    return render(request, 'fixtures.html')

def results(request):
    return render(request, 'results.html')



# In your views.py file
def organizer_dashboard(request):
    tournaments = Tournament.objects.all()  # Fetch all tournaments
    return render(request, 'organizer_dashboard.html', {'tournaments': tournaments})

from .forms import TournamentForm

def add_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organizer_dashboard')  # Redirect to the tournament dashboard
    else:
        form = TournamentForm()
    return render(request, 'add_tournament.html', {'form': form})

def loginorg_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('organizer_dashboard')  # Redirect to the tournament dashboard page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import Tournament  # Assuming you have a Tournament model

def submit_tournament(request):
    if request.method == 'POST':
        name = request.POST['name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        # Create a new tournament instance and save it
        tournament = Tournament(name=name, start_date=start_date, end_date=end_date)
        tournament.save()
        return redirect('organizer_dashboard')  # Redirect to the dashboard or another page
    return render(request, 'add_tournament.html')  # Render the form if not a POST request

# events/views.py
from django.shortcuts import render, get_object_or_404
from .models import Tournament  # Assuming you have a Tournament model

def tournament_detail(request, id):
    tournament = get_object_or_404(Tournament, id=id)
    return render(request, 'tournament_detail.html', {'tournament': tournament})


def results_view(request):
    # Your logic here
    return render(request, 'results.html')


def registered_players(request):
    players = PlayerRegistration.objects.all()
    return render(request, 'registered_players.html', {'players': players})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tournament, PlayerRegistration

@login_required
def tournament_registration(request):
    if request.method == 'POST':
        # Retrieve form data
        tournament_id = request.POST.get('tournament_id')
        player_name = request.POST.get('name')
        player_email = request.POST.get('email')
        player_age = request.POST.get('age')
        player_weight_category = request.POST.get('weight-category')

        # Validate and save the data
        if tournament_id and player_name and player_email and player_age and player_weight_category:
            try:
                tournament = Tournament.objects.get(id=tournament_id)

                # Check if the user has already registered for this tournament
                existing_registration = PlayerRegistration.objects.filter(
                    tournament=tournament,
                    player_email=player_email  # Assuming email is unique per user
                ).exists()

                if existing_registration:
                    return render(request, 'tournament_registration.html', {
                        'error': 'You have already registered for this tournament.',
                        'tournament': tournament
                    })

                # If no existing registration, proceed to save
                player_registration = PlayerRegistration(
                    tournament=tournament,
                    player_name=player_name,
                    player_email=player_email,
                    player_age=player_age,
                    player_weight_category=player_weight_category
                )
                player_registration.save()
                return redirect('tournament_dashboard')  # Redirect to the dashboard after successful registration

            except Tournament.DoesNotExist:
                return render(request, 'tournament_registration.html', {'error': 'Invalid tournament ID'})
        else:
            return render(request, 'tournament_registration.html', {'error': 'All fields are required'})
    else:
        # Handle GET request (display the form)
        tournament_id = request.GET.get('tournament_id')
        if tournament_id:
            try:
                tournament = Tournament.objects.get(id=tournament_id)
                return render(request, 'tournament_registration.html', {'tournament': tournament})
            except Tournament.DoesNotExist:
                return render(request, 'tournament_registration.html', {'error': 'Invalid tournament ID'})
        else:
            return render(request, 'tournament_registration.html')
    
def registered_players(request):
    tournament_id = request.GET.get('tournament_id')
    if tournament_id:
        tournament = Tournament.objects.get(id=tournament_id)
        players = PlayerRegistration.objects.filter(tournament=tournament)
        return render(request, 'registered_players.html', {'players': players})
    else:
        return render(request, 'registered_players.html', {'players': PlayerRegistration.objects.all()})
    
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def player_profile(request):
    user = request.user
    return render(request, 'player_profile.html', {'user': user})