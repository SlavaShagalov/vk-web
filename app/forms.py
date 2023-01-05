from django.core.exceptions import ValidationError

from django import forms
from django.core.validators import validate_email
from django.forms import CharField

from django.contrib.auth.models import User
from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = CharField(widget=forms.TextInput())
    password = CharField(widget=forms.PasswordInput(render_value=True), min_length=3)


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(), label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), min_length=3)
    password_check = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        for field in ['username', 'first_name', 'last_name', 'email', 'password', 'password_check']:
            if field not in self.cleaned_data.keys():
                return self.cleaned_data

        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            self.add_error('password_check', 'Password do not match')

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'A user with such email already exists')

        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'A user with such username already exists')

        return self.cleaned_data

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(**self.cleaned_data)
        profile = Profile.objects.create(user=user)
        profile.save()
        return profile


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(label="Avatar image", required=False, widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

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
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "django postgres"}), label="Tags",
                           required=False)

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "How to change element color?"}),
            'text': forms.Textarea(attrs={"placeholder": "I got an error..."}),
        }
        # error_messages = {
        #     NON_FIELD_ERRORS: {
        #         'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
        #     }
        # }

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tag_list = data.split()
        for tag in tag_list:
            if len(tag) > 32:
                self.add_error('tags', 'Max length of tag is 32 characters')
        return data

    def save(self, profile):
        question = super().save(commit=False)
        question.profile = profile
        question.save()
        data = self.cleaned_data['tags']
        tag_list = data.split()
        for tag in tag_list:
            question.tags.add(Tag.objects.get_or_create(name=tag)[0].id)
        question.save()

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={"placeholder": "My solution is..."}),
        }
