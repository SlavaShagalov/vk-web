from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class ProfileManager(models.Manager):
    def top_users(self, count=5):
        return self.annotate(n_answers=Count('answer')).order_by('-n_answers')[:count]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(null=True, blank=True, default='/static/img/avatars/no-avatar.jpeg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def top_tags(self, count=10):
        return self.annotate(que_count=Count('question')).order_by('-que_count')[:count]


class Tag(models.Model):
    name = models.CharField(max_length=32)
    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def annotate_n_ans_rating(self):
        return self.annotate(n_answers=Count('answer', distinct=True),
                             rating=Count('questionlike', distinct=True) - Count('questiondislike', distinct=True))

    def new(self):
        return self.annotate_n_ans_rating().order_by('-publish_date')

    def hot(self):
        return self.annotate_n_ans_rating().order_by('-rating')

    def by_tag(self, tag):
        return self.annotate_n_ans_rating().filter(tags__name=tag)

    def by_id(self, id):
        return self.annotate_n_ans_rating().get(id=id)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    objects = QuestionManager()


class AnswerManager(models.Manager):
    def annotate_rating(self):
        return self.annotate(rating=Count('answerlike', distinct=True) - Count('answerdislike', distinct=True))

    def by_question(self, que_id):
        return self.annotate_rating().order_by('publish_date').filter(question_id=que_id)


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class QuestionDislike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class AnswerDislike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
