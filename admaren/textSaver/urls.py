from django.urls import path

from textSaver.views import (LoginView, OverView, Tagdetail, TagList,
                             Textdetail, TextView, UserView)

urlpatterns = [

    path('register/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('tags/', TagList.as_view()),
    path('tags/<int:pk>/', Tagdetail.as_view()),
    path('texts/', TextView.as_view()),
    path('texts/<int:pk>/', Textdetail.as_view()),
    path('overview/', OverView.as_view())
]
