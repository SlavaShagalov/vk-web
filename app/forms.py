from django.core.exceptions import ValidationError

from django import forms
from django.core.validators import validate_email
from django.forms import CharField

from django.contrib.auth.models import User
from app.models import Profile, Question, Label, Answer


class LoginForm(forms.Form):
    username = CharField(widget=forms.TextInput(), label='Логин:')
    password = CharField(widget=forms.PasswordInput(render_value=True), min_length=3, label='Пароль:')


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(), label='Email:', required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), min_length=3, label='Пароль:')
    password_check = forms.CharField(widget=forms.PasswordInput(render_value=True), label='Повтор пароля:')
    avatar = forms.ImageField(label='Фото профиля:', required=False, widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

        labels = {
            'username': 'Login:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:'
        }

    def clean(self):
        if 'password' not in self.cleaned_data.keys() or 'password_check' not in self.cleaned_data.keys():
            return self.cleaned_data

        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            self.add_error('password_check', 'Password do not match')

        return self.cleaned_data

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            self.add_error('username', 'A user with such username already exists')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            self.add_error('email', 'A user with such email already exists')
        return data

    def save(self, **kwargs):
        avatar = None
        # print(self.cleaned_data['avatar'])
        if 'avatar' in self.cleaned_data.keys():
            avatar = self.cleaned_data['avatar']

        self.cleaned_data.pop('password_check')
        self.cleaned_data.pop('avatar')
        user = User.objects.create_user(**self.cleaned_data)

        profile = Profile.objects.create(user=user)
        if avatar:
            profile.avatar = avatar
        profile.save()
        return profile


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(label='Фото профиля:', required=False, widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        labels = {
            'username': 'Login:',
            'email': 'Email:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:'
        }

    def clean(self):
        cleaned_data = super().clean()

        if len(self.changed_data) == 0:
            return cleaned_data

        if 'email' in self.cleaned_data.keys():
            if len(cleaned_data['email']) == 0:
                self.add_error('email', "This field is required.")
            elif 'username' in self.cleaned_data.keys() and \
                    'email' in self.changed_data and \
                    User.objects.exclude(username=self.cleaned_data['username']).filter(
                        email=self.cleaned_data['email']).exists():
                self.add_error('email', 'A user with such email already exists')

        return cleaned_data

    def save(self, **kwargs):
        user = super().save()

        profile = user.profile
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return user


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "django postgres"}), label='Tags:',
                           required=False)

    class Meta:
        model = Question
        fields = ['title', 'text']

        labels = {
            'title': 'Title:',
            'text': 'Text:',
        }

        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "How to change element color?"}),
            'text': forms.Textarea(attrs={"placeholder": "I got an error..."}),
        }

    def clean_tags(self):
        data = self.cleaned_data['labels']
        tag_list = data.split()
        for tag in tag_list:
            if len(tag) > 32:
                self.add_error('labels', 'Max length of tag is 32 characters')
        return data

    def save(self, profile):
        question = super().save(commit=False)
        question.profile = profile
        question.save()
        data = self.cleaned_data['labels']
        tag_list = data.split()
        for tag in tag_list:
            question.labels.add(Label.objects.get_or_create(name=tag)[0].id)
        question.save()

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        labels = {
            'text': '',
        }

        widgets = {
            'text': forms.Textarea(attrs={"placeholder": "My solution is..."}),
        }
