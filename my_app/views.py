
from django.shortcuts import render, redirect
from django.contrib import messages
from my_app.models import Room
from my_app.models import User

# Create your views here.
def index(request):
    if request.method == 'POST':
        roomId = request.POST.get("room-id", None) #get from the "form" in the index.html
        playerId = request.POST.get("user-id", None)
        
        if(roomId):
            try: 
                room = Room.objects.get(roomNumber=roomId)
                return redirect(f"/game/{room.roomNumber}/{playerId}/") #send to this endpoint
            except Room.DoesNotExist:
                room = Room(roomNumber=roomId)
                room.save() #create new model in the "models.py"
                return redirect(f"/game/{room.roomNumber}/{playerId}/")
        else:
            messages.error(request, "You need to choose a room!")
            return redirect("index") #send to this endpoint 

    
    return render(request, "index.html")


def game(request, roomNumber=None, playerId=None):
    try:
        room = Room.objects.get(roomNumber=roomNumber)
        player = User.objects.get(id=playerId).username
        playerId = User.objects.get(id=playerId).id
        return render(request, "game.html", {"room": room, "playerId": playerId, "player": player  }) #this will be send to the browser to ew get in the html page those attributes
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist, fool!")
        return redirect("login/")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create a new player
        user = User(username=username, email=email, password=password)
        user.save()

        # Redirect to a success page or perform any other actions
        return redirect('login')

    return render(request, 'register.html')
    

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Retrieve the player by username
            user = User.objects.get(username=username)

            # Check if the provided password matches
            if user.password == password:
                # Perform any login-related actions (e.g., set session variables)
                request.session['username'] = user.username
                request.session['user_id'] = user.id
                return redirect('index')
            else:
                # Handle invalid credentials
                return redirect('login')
        except User.DoesNotExist:
            # Handle invalid credentials
            return redirect('register')

    return render(request, 'login.html')


def logoutPage(request):
    return redirect('login')