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


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()
    old_password = forms.CharField()
    def __init__(self, *args,user = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Неправельный пароль!")
        return old_password


class PasswordResetForm(forms.Form):
    password = forms.CharField()
    password_confirm = forms.CharField()
    def __init__(self, *args,user = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    def clean(self):
        clean_data = super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен быть больше 8 символов")
        if len(password) > 128:
            raise forms.ValidationError("Пароль не может быть больше 128 символов")
        if self.user.check_password(password):
            raise forms.ValidationError("Такой пароль стоит щас у вас")
        return clean_data