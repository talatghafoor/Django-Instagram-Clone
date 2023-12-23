from chat.views import inbox, Directs, SendDirect, UserSearch, NewConversation
from django.urls import path

urlpatterns = [
    path('', inbox, name="message"),
    path('chat/<username>', Directs, name="chat"),
    path('send/', SendDirect, name="send-chat"),
    path('search/', UserSearch, name="search-users"),
    path('new/<username>', NewConversation, name="conversation"),
]