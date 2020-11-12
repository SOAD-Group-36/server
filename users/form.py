from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
