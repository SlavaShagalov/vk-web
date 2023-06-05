from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from django.forms import model_to_dict
from app.forms import LoginForm, RegistrationForm, SettingsForm, QuestionForm, AnswerForm
from app.models import Question, Label, Profile, Answer, Score

from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from utils import paginate


@require_GET
def index(request):
    # print('home')
    context = {
        'title': 'Новые вопросы',
        'page_obj': paginate(Question.objects.new(), request, 5),
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
    }
    return render(request, 'index.html', context=context)


@require_GET
def hot_questions(request):
    context = {
        'title': 'Популярные вопросы',
        'page_obj': paginate(Question.objects.hot(), request, 5),
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
    }
    return render(request, 'index.html', context=context)


@require_GET
def questions_by_label(request, label: str):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
    }
    questions = Question.objects.by_label(label)
    if questions.count() == 0:
        return render(request, "not_found.html", context, status=404)
    page_obj = paginate(questions, request, 5)
    context.update({
        'title': f'Метка: {label}',
        "page_obj": page_obj,
    })
    return render(request, 'index.html', context=context)


@require_http_methods(['GET', 'POST'])
def question(request, q_id: int):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
    }

    try:
        quest = Question.objects.by_id(q_id)
        page_obj = paginate(Answer.objects.by_question(q_id), request, 5)
        context.update({
            "question": quest,
        })
    except ObjectDoesNotExist:
        return render(request, "not_found.html", context, status=404)

    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login?continue={request.path}')
        else:
            form = AnswerForm(data=request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                profile = Profile.objects.get(user=request.user)

                answer.profile = profile
                answer.question = quest
                answer.save()

                page_obj = paginate(Answer.objects.by_question(q_id), request, 5)
                return redirect(f"{request.path}?page={page_obj.paginator.num_pages}#{answer.id}")
    context.update({
        "page_obj": page_obj,
        "form": form,
    })
    return render(request, 'question.html', context=context)


@require_http_methods(['GET', 'POST'])
@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    if request.method == "GET":
        form = QuestionForm()
    elif request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            question = form.save(profile)
            return redirect('question', q_id=question.id)
    else:
        form = {}
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
        'form': form,
    }
    return render(request, 'ask.html', context=context)


@require_http_methods(['GET', 'POST'])
def login(request):
    next_url = request.GET.get('continue')
    next_url = next_url if next_url else 'home'
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'GET':
        form = LoginForm()
        cache.set('continue', next_url)
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request=request, **form.cleaned_data)
            if user:
                auth.login(request, user)

                next_url = cache.get('continue')
                cache.delete('continue')
                next_url = next_url if next_url else 'home'
                return redirect(next_url)
            else:
                form.add_error(None, "Неправильный логин или пароль.")
                form.add_error('username', "")
                form.add_error('password', "")
    else:
        form = {}
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
        'form': form
    }
    return render(request, 'login.html', context=context)


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        form = RegistrationForm()
    elif request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            auth.login(request, profile.user)
            return redirect('home')
    else:
        form = {}
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
        'form': form,
    }
    return render(request, 'signup.html', context=context)


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = SettingsForm(initial=initial_data)
    elif request.method == "POST":
        form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))
    else:
        form = {}
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_labels': Label.objects.top_labels(10),
        'form': form,
    }
    return render(request, 'settings.html', context=context)


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@require_http_methods(['POST', 'OPTIONS'])
def vote(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "error",
        })

    object_id = request.POST['object_id']
    object_type = request.POST['object_type']
    vote_value = request.POST['vote_value']
    profile_id = request.user.profile.id

    try:
        rating = Score.objects.add_score(score_value=int(vote_value), profile_id=profile_id, object_id=object_id,
                                         object_type=int(object_type))
        return JsonResponse({
            "status": "ok",
            "rating": rating,
        })
    except:
        return JsonResponse({
            "status": "error",
        })


@require_http_methods(['POST', 'OPTIONS'])
def correct(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "error",
        })

    question_id = request.POST['question_id']
    answer_id = request.POST['answer_id']

    new_correct = Answer.objects.get(id=answer_id, question_id=question_id)
    new_state = not new_correct.correct

    try:
        old_correct = Answer.objects.get(question_id=question_id, correct=True)
        old_correct.correct = False
        old_correct.save()
    except Answer.DoesNotExist:
        print('Not found old correct answer')

    new_correct.correct = new_state
    new_correct.save()

    return JsonResponse({
        "status": "ok",
        "new_state": new_state,
    })
