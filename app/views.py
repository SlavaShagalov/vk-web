from django.shortcuts import render, redirect
from app.models import Question, Tag, Profile, Answer
from django.db import models

from django.core.exceptions import ObjectDoesNotExist

from utils import paginate

cur_user = {'is_auth': True}


def index(request):
    context = {
        'title': 'New Questions',
        'page_obj': paginate(Question.objects.new(), request, 5),
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': cur_user['is_auth'],
    }
    return render(request, 'index.html', context=context)


def hot_questions(request):
    context = {
        'title': 'Hot Questions',
        'page_obj': paginate(Question.objects.hot(), request, 5),
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': cur_user['is_auth'],
    }
    return render(request, 'index.html', context=context)


def questions_by_tag(request, tag: str):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': cur_user['is_auth'],
    }
    questions = Question.objects.by_tag(tag)
    if questions.count() == 0:
        return render(request, "not_found.html", context, status=404)
    page_obj = paginate(questions, request, 5)
    context.update({
        'title': f'Tag: {tag}',
        "page_obj": page_obj,
    })
    return render(request, 'index.html', context=context)


def question(request, q_id: int):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': cur_user['is_auth'],
    }
    try:
        q = Question.objects.by_id(q_id)
        page_obj = paginate(Answer.objects.by_question(q_id), request, 5)
        context.update({
            "question": q,
            "page_obj": page_obj,
        })
    except ObjectDoesNotExist:
        return render(request, "not_found.html", context, status=404)
    return render(request, 'question.html', context=context)


def ask(request):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': cur_user['is_auth'],
    }
    return render(request, 'ask.html', context=context)


def login(request):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': False,
    }
    return render(request, 'login.html', context=context)


def signup(request):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': False,
    }
    return render(request, 'signup.html', context=context)


def settings(request):
    context = {
        'best_members': Profile.objects.top_users(10),
        'popular_tags': Tag.objects.top_tags(10),
        'is_auth': True,
    }
    return render(request, 'settings.html', context=context)


def logout(request):
    cur_user['is_auth'] = False
    return redirect(index)
