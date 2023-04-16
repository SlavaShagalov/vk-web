from django.urls import path

from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag>', views.questions_by_label, name='tag'),
    path('question/<int:q_id>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('profile/edit/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('vote/', views.vote, name='vote'),
    path('correct/', views.correct, name='correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
