from django.contrib import admin
from app.models import Question, Answer, Profile, Label, Vote

admin.site.register(Profile)
admin.site.register(Label)
admin.site.register(Vote)
admin.site.register(Question)
admin.site.register(Answer)
