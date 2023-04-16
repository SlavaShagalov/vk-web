from django.core.management.base import BaseCommand
from app.models import Question, Profile, Vote, Label, Answer
from django.contrib.auth.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Vote.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Label.objects.all().delete()
