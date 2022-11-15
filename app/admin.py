from django.contrib import admin
from app.models import Question, Answer, Profile, Tag, QuestionLike, QuestionDislike, AnswerLike, AnswerDislike

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(QuestionLike)
admin.site.register(QuestionDislike)
admin.site.register(AnswerLike)
admin.site.register(AnswerDislike)
