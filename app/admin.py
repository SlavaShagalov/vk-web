from django.contrib import admin
from app.models import Question, Answer, Profile, Tag, Vote

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Question)
admin.site.register(Answer)
