from django.urls import path
from .views import current_user, UserList, CurrentRoom, CurrentGame, current_game_data, current_room_data, CreateHand

urlpatterns = [
    path('current_user/', current_user),
    path('current_game_data/', current_game_data),
    path('current_room/', current_room_data),
    path('current_game/', CurrentGame.as_view()),
    path('submit_hand/', CreateHand.as_view()),
    path('users/', UserList.as_view())
]