from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db.models import Count, Sum


class ProfileManager(models.Manager):
    def top_users(self, count=5):
        return self.annotate(n_answers=Count('answer')).order_by('-n_answers')[:count]


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
        return self.annotate(n_questions=Count('question')).order_by('-n_questions')[:count]


class Label(models.Model):
    name = models.CharField(max_length=32, verbose_name='Label name', unique=True)

    objects = LabelManager()

    def __str__(self):
        return self.name


class ScoreManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(score__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(score__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('score')).get('score__sum') or 0

    def questions(self):
        return self.get_queryset().filter(content_type__model='question').order_by('-questions__pub_date')

    def answers(self):
        return self.get_queryset().filter(content_type__model='answer').order_by('-answers__pub_date')

    def add_score(self, score_value, profile_id, object_id, object_type):
        obj = None
        if object_type == 0:
            obj = Question.objects.get(id=object_id)
            object_type = 'question'
        elif object_type == 1:
            obj = Answer.objects.get(id=object_id)
            object_type = 'answer'

        try:
            score = self.get(profile_id=profile_id, content_type__model=object_type, object_id=object_id)
        except Score.DoesNotExist:
            score = None

        # если пользователь хочет сделать, например, дизлайк вместо лайка, нужно нажать два раза на дизлайк
        # - первый, чтоб отменить лайк, второй, чтобы поставить дизлайк
        if not score:
            self.create(score=score_value, profile_id=profile_id, content_object=obj)
        elif score.score == score_value:
            raise Exception
        else:
            score.delete()

        obj.rating += score_value
        obj.save()
        return obj.rating


class Score(models.Model):
    LIKE = 1
    DISLIKE = -1

    SCORES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    score_value = models.SmallIntegerField(verbose_name='Score', choices=SCORES)

    profile = models.ForeignKey(to=Profile, verbose_name='Profile', related_name='score', on_delete=models.CASCADE)

    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = ScoreManager()

    class Meta:
        # пользователь не может проголосовать более одного раза за одну сущность (вопрос/ответ):
        # - исключается возможноть накручивать много лайков/дизлайков
        # - исключается возможноть одновременного лайка и дизлайка от одного пользователя за одну сущность
        unique_together = ('profile', 'content_type', 'object_id')


class QuestionManager(models.Manager):
    def annotate_n_answers(self):
        return self.annotate(n_answers=Count('answer', distinct=True))

    def new(self):
        return self.annotate_n_answers().order_by('-pub_date')

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
    scores = GenericRelation(to=Score, related_query_name='question')

    objects = QuestionManager()

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["rating"])
        ]

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def by_question(self, question_id):
        return self.filter(question_id=question_id).order_by('pub_date')


class Answer(models.Model):
    text = models.TextField(verbose_name='Answer text', blank=False)
    correct = models.BooleanField(default=False, verbose_name='Answer correct')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Answer publish date')
    rating = models.IntegerField(default=0)

    profile = models.ForeignKey(to=Profile, related_name='answer', null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(to=Question, related_name='answer', on_delete=models.CASCADE)
    scores = GenericRelation(to=Score, related_query_name='answer')

    objects = AnswerManager()

    def __str__(self):
        return self.text
