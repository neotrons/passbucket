from django import forms
from django.contrib.auth import authenticate
from .models import Bucket
from core.aescrypt import AESCrypt


class BucketForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = Bucket
        fields = ('password', 'name', 'user_account', 'password_account', 'recovery_email', 'recovery_phone',
                  'secret_question', 'secret_response')
        """
        widgets = {
            'clave': forms.PasswordInput(render_value=True),
            'email_recuperacion': forms.PasswordInput(render_value=True),
            'telefono_recuperacion': forms.PasswordInput(render_value=True),
            'pregunta_secreta': forms.PasswordInput(render_value=True),
            'respuesta_secreta': forms.PasswordInput(render_value=True),
        }"""

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = authenticate(username=self.request.user.username, password=password)
        if user is not None:
            return password
        else:
            raise forms.ValidationError("The password does not match the login")

    def save(self, commit=True):
        self.instance = super(BucketForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        password_account = self.cleaned_data.get('password_account')
        recovery_email = self.cleaned_data.get('recovery_email')
        recovery_phone = self.cleaned_data.get('recovery_phone')
        secret_question = self.cleaned_data.get('secret_question')
        secret_response = self.cleaned_data.get('secret_response')

        if self.instance.id is not None:
            bucket = Bucket.objects.get(id=self.instance.id)
            if bucket.clave != password_account:
                self.instance.password_account = AESCrypt(password).encrypt(password_account)

            if bucket.recovery_email != recovery_email:
                self.instance.recovery_email = AESCrypt(password).encrypt(recovery_email)

            if bucket.recovery_phone != recovery_phone:
                self.instance.recovery_phone = AESCrypt(password).encrypt(recovery_phone)

            if bucket.secret_question != secret_question:
                self.instance.secret_question = AESCrypt(password).encrypt(secret_question)

            if bucket.secret_response != secret_response:
                self.instance.secret_response = AESCrypt(password).encrypt(secret_response)

        else:
            self.instance.password_account = AESCrypt(password).encrypt(password_account)
            self.instance.recovery_phone = AESCrypt(password).encrypt(recovery_phone)
            self.instance.recovery_phone = AESCrypt(password).encrypt(recovery_phone)
            self.instance.secret_question = AESCrypt(password).encrypt(secret_question)
            self.instance.secret_response = AESCrypt(password).encrypt(secret_response)

        if commit:
            self.instance.save()
        else:
            return self.instance
