from django.contrib import admin
from app.models import Question, Answer, Profile, Label, QuestionScore, AnswerScore

admin.site.register(Profile)
admin.site.register(Label)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionScore)
admin.site.register(AnswerScore)
