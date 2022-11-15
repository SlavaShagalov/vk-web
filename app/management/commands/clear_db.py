from django.core.management.base import BaseCommand
from app.models import Question, Profile, QuestionLike, QuestionDislike, AnswerLike, AnswerDislike, Tag, Answer
from django.contrib.auth.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        AnswerLike.objects.all().delete()
        AnswerDislike.objects.all().delete()
        QuestionLike.objects.all().delete()
        QuestionDislike.objects.all().delete()
