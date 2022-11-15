from django.core.management.base import BaseCommand
from app.models import Question, Profile, Tag, Answer, QuestionLike, QuestionDislike, AnswerLike, AnswerDislike
from django.contrib.auth.models import User

from faker import Faker
import random

DEFAULT_N_USERS = 1
DEFAULT_N_QUESTIONS = 10
DEFAULT_N_ANSWERS = 100
DEFAULT_N_TAGS = 1
DEFAULT_N_LIKES = 200


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--ratio')

    def handle(self, *args, **options):
        ratio = int(options['ratio']) if options['ratio'] else 10000

        self.users_gen(ratio * DEFAULT_N_USERS)
        self.tags_gen(ratio * DEFAULT_N_TAGS)
        self.questions_gen(ratio * DEFAULT_N_QUESTIONS)
        self.answers_gen(ratio * DEFAULT_N_ANSWERS)
        self.likes_dislikes_gen(ratio * DEFAULT_N_LIKES)

    def users_gen(self, count):
        print("Users generating...")
        users = [None] * count
        profiles = [None] * count
        for i in range(count):
            username = self.faker.unique.user_name()
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = self.faker.email()
            password = self.faker.password()
            user = User(username=username, first_name=first_name,
                        last_name=last_name, email=email, password=password)
            avatar = f'/static/img/avatars/avatar-{random.randint(1, 9)}.jpg'

            users[i] = user
            profiles[i] = Profile(user=user, avatar=avatar)
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        print('Success.')

    def tags_gen(self, count):
        print("Tags generating...")
        tags = [None] * count
        for i in range(count):
            tag_name = self.faker.word()

            tags[i] = Tag(name=tag_name)
        Tag.objects.bulk_create(tags)
        print("Success.")

    def questions_gen(self, count):
        print("Questions generating...")
        prof_min_id = Profile.objects.order_by('id')[0].id
        prof_max_id = Profile.objects.order_by('-id')[0].id
        tag_min_id = Tag.objects.order_by('id')[0].id
        tag_max_id = Tag.objects.order_by('-id')[0].id

        questions = [None] * count
        for i in range(count):
            title = self.faker.paragraph(1)[:-1] + '?'
            text = self.faker.paragraph(random.randint(5, 20))
            profile_id = random.randint(prof_min_id, prof_max_id)

            questions[i] = Question(text=text, title=title, profile_id=profile_id)
        questions = Question.objects.bulk_create(questions)

        tags = [None] * 10
        for i in range(count):
            n_tags = random.randint(1, 5)
            for j in range(n_tags):
                tags[j] = Tag.objects.get(id=random.randint(tag_min_id, tag_max_id))
            questions[i].tags.add(*tags[:n_tags])
        print("Success.")

    def answers_gen(self, count):
        print("Answers generating...")
        prof_min_id = Profile.objects.order_by('id')[0].id
        prof_max_id = Profile.objects.order_by('-id')[0].id
        que_min_id = Question.objects.order_by('id')[0].id
        que_max_id = Question.objects.order_by('-id')[0].id

        answers = [None] * count
        for i in range(count):
            text = self.faker.paragraph(random.randint(5, 20))
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)

            answers[i] = Answer(text=text, profile_id=profile_id, question_id=question_id)
        Answer.objects.bulk_create(answers)
        print("Success.")

    def likes_dislikes_gen(self, count):
        print('Question likes/dislikes generating...')
        prof_min_id = Profile.objects.order_by('id')[0].id
        prof_max_id = Profile.objects.order_by('-id')[0].id
        que_min_id = Question.objects.order_by('id')[0].id
        que_max_id = Question.objects.order_by('-id')[0].id

        n_q_likes = count // 4
        q_likes = [None] * n_q_likes
        used_pairs = []
        for j in range(n_q_likes):
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            while (profile_id, question_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                question_id = random.randint(que_min_id, que_max_id)

            q_likes[j] = QuestionLike(profile_id=profile_id, question_id=question_id)
            used_pairs.append((profile_id, question_id))
        QuestionLike.objects.bulk_create(q_likes)

        n_q_dislikes = count // 4
        q_dislikes = [None] * n_q_dislikes
        for j in range(n_q_dislikes):
            profile_id = random.randint(prof_min_id, prof_max_id)
            question_id = random.randint(que_min_id, que_max_id)
            while (profile_id, question_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                question_id = random.randint(que_min_id, que_max_id)

            q_dislikes[j] = QuestionDislike(profile_id=profile_id, question_id=question_id)
            used_pairs.append((profile_id, question_id))
        QuestionDislike.objects.bulk_create(q_dislikes)
        print("Success.")

        print("Answer likes/dislikes generating...")
        ans_min_id = Answer.objects.order_by('id')[0].id
        ans_max_id = Answer.objects.order_by('-id')[0].id

        n_a_likes = count // 4
        a_likes = [None] * n_a_likes
        used_pairs = []
        for j in range(n_a_likes):
            profile_id = random.randint(prof_min_id, prof_max_id)
            answer_id = random.randint(ans_min_id, ans_max_id)
            while (profile_id, answer_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                answer_id = random.randint(ans_min_id, ans_max_id)

            a_likes[j] = AnswerLike(profile_id=profile_id, answer_id=answer_id)
            used_pairs.append((profile_id, answer_id))
        AnswerLike.objects.bulk_create(a_likes)

        n_a_dislikes = count - n_a_likes * 3
        a_dislikes = [None] * n_a_dislikes
        for j in range(n_a_dislikes):
            profile_id = random.randint(prof_min_id, prof_max_id)
            answer_id = random.randint(ans_min_id, ans_max_id)
            while (profile_id, answer_id) in used_pairs:
                profile_id = random.randint(prof_min_id, prof_max_id)
                answer_id = random.randint(ans_min_id, ans_max_id)

            a_dislikes[j] = AnswerDislike(profile_id=profile_id, answer_id=answer_id)
            used_pairs.append((profile_id, answer_id))
        AnswerDislike.objects.bulk_create(a_dislikes)
        print("Success.")
