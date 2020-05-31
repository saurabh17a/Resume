from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile as User
# User = settings.AUTH_USER_MODEL


choice_type = (
    ('Candidate', 'Candidate'),
    ('Recruiter', 'Recruiter'),
)


class NewUser(UserCreationForm):
    user_types = forms.ChoiceField(choices=choice_type)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "user_types")

    def save(self, commit=True):
        user = super(NewUser, self).save(commit=False)
        user.user_types = self.cleaned_data["user_types"]
        if commit:
            user.save()
        return user
