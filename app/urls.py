from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag>', views.questions_by_tag, name='tag'),
    path('question/<int:q_id>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
]
