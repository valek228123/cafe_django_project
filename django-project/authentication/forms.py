from django import forms

from authentication.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']
        # widgets = {
        #     'username': forms.TextInput(attrs={ 'help_text': "" }),
        # }
    def clean(self):
        cleand_data = super().clean()
        username = cleand_data.get('username')
        password = cleand_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Вы передали не корректные данные, попробуйте еще раз, поменяв данные!!!")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже сушетвует")
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен быть больше 8 символов')
        if len(username) > 150:
            raise forms.ValidationError("Имя пользователя не может быть больше 150 символов")
        if len(password) > 128:
            raise forms.ValidationError("Пароль не может быть больше 128 символов")
        return cleand_data

