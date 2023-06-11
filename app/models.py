from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count


class ProfileManager(models.Manager):
    def top_users(self, count=5):
        return self.using('guest').annotate(n_answers=Count('answer')).order_by('-n_answers')[:count]


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, verbose_name='Profile avatar',
                               default='/avatar/default_avatar.jpeg',
                               upload_to='avatar/%Y/%m/%d/')

    user = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE, null=False)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class LabelManager(models.Manager):
    def top_labels(self, count=10):
        return self.using('guest').annotate(n_questions=Count('question')).order_by('-n_questions')[:count]


class Label(models.Model):
    name = models.CharField(max_length=32, verbose_name='Label name', unique=True)

    objects = LabelManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def annotate_n_answers(self):
        return self.annotate(n_answers=Count('answer', distinct=True))

    def new(self):
        return self.annotate_n_answers().order_by('-created_at')

    def hot(self):
        return self.annotate_n_answers().order_by('-rating')

    def by_label(self, label):
        return self.annotate_n_answers().filter(labels__name=label)

    def by_id(self, id):
        return self.annotate_n_answers().get(id=id)


class Question(models.Model):
    title = models.CharField(max_length=256, verbose_name='Question title', blank=False)
    text = models.TextField(verbose_name='Question text', blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Question created time')
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(to=Profile, related_name='question', null=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(to=Label, related_name='question', blank=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def by_question(self, question_id):
        return self.using('guest').filter(question_id=question_id).order_by('created_at')


class Answer(models.Model):
    text = models.TextField(verbose_name='Answer text', blank=False)
    correct = models.BooleanField(default=False, verbose_name='Answer correct')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Answer created time')
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(to=Profile, related_name='answer', null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(to=Question, related_name='answer', on_delete=models.CASCADE)

    objects = AnswerManager()

    def __str__(self):
        return self.text


class QuestionScoreManager(models.Manager):
    def add_score(self, value, profile_id, question_id):
        try:
            score = self.get(profile_id=profile_id, question_id=question_id)
        except QuestionScore.DoesNotExist:
            score = None

        # если пользователь хочет сделать, например, дизлайк вместо лайка, нужно нажать два раза на дизлайк
        # - первый, чтоб отменить лайк, второй, чтобы поставить дизлайк
        if not score:
            print(f"QUESTION_SCORE_CREATE: profile_id={profile_id}, question_id={question_id}, value={value}")
            self.create(value=value, profile_id=profile_id, question_id=question_id)
        elif score.value == value:
            print(f"QUESTION_SCORE_ALREADY_EXISTS: profile_id={profile_id}, question_id={question_id}, value={value}")
            raise Exception
        else:
            print(f"QUESTION_SCORE_DELETE: profile_id={profile_id}, question_id={question_id}")
            score.delete()  # отмена лайка

        question = Question.objects.get(id=question_id)
        return question.rating


class QuestionScore(models.Model):
    SCORES = [
        (1, 'Positive'),
        (-1, 'Negative'),
    ]

    value = models.SmallIntegerField(verbose_name='Value', choices=SCORES)

    question = models.ForeignKey(to=Question, related_name='questionscore', on_delete=models.CASCADE)
    profile = models.ForeignKey(to=Profile, verbose_name='Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionScoreManager()

    class Meta:
        unique_together = ('profile', 'question')


class AnswerScoreManager(models.Manager):
    def add_score(self, value, profile_id, answer_id):
        try:
            score = self.get(profile_id=profile_id, answer_id=answer_id)
        except AnswerScore.DoesNotExist:
            score = None

        # если пользователь хочет сделать, например, дизлайк вместо лайка, нужно нажать два раза на дизлайк
        # - первый, чтоб отменить лайк, второй, чтобы поставить дизлайк
        if not score:
            print(f"ANSWER_SCORE_CREATE: profile_id={profile_id}, answer_id={answer_id}, value={value}")
            self.create(value=value, profile_id=profile_id, answer_id=answer_id)
        elif score.value == value:
            print(f"ANSWER_SCORE_ALREADY_EXISTS: profile_id={profile_id}, answer_id={answer_id}, value={value}")
            raise Exception
        else:
            print(f"ANSWER_SCORE_DELETE: profile_id={profile_id}, answer_id={answer_id}")
            score.delete()  # отмена лайка

        answer = Answer.objects.get(id=answer_id)
        return answer.rating


class AnswerScore(models.Model):
    SCORES = [
        (1, 'Positive'),
        (-1, 'Negative'),
    ]

    value = models.SmallIntegerField(verbose_name='Score', choices=SCORES)

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(to=Profile, verbose_name='Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerScoreManager()

    class Meta:
        unique_together = ('profile', 'answer')
