from django.contrib import admin
from app.models import Question, Answer, Profile, Label, Score

admin.site.register(Profile)
admin.site.register(Label)
admin.site.register(Score)
admin.site.register(Question)
admin.site.register(Answer)
