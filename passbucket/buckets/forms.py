from django import forms
from django.contrib.auth import authenticate
from .models import Bucket
from core.aescrypt import AESCrypt


class BucketForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    is_decrypt = forms.BooleanField(required=False)

    class Meta:
        model = Bucket
        fields = ('password', 'is_decrypt', 'name', 'user_account', 'password_account', 'recovery_email',
                  'recovery_phone', 'secret_question', 'secret_response')
        widgets = {
            'password_account': forms.PasswordInput(render_value=True),
            'email_recuperacion': forms.PasswordInput(render_value=True),
            'telefono_recuperacion': forms.PasswordInput(render_value=True),
            'pregunta_secreta': forms.PasswordInput(render_value=True),
            'respuesta_secreta': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super(BucketForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.fields['is_decrypt'].widget.attrs.update({"readonly": "readonly",
                                                           "onclick": "javascript: return false;"})

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
        is_decrypt = self.cleaned_data.get('is_decrypt')
        no_encript_list = ['name', 'user_account']
        key = AESCrypt(password)
        if self.instance.id is not None:
            bucket = Bucket.objects.get(id=self.instance.id)
            for field in self.fields:
                value = self.cleaned_data.get(field)
                if not is_decrypt and getattr(bucket, field, None) != value and hasattr(bucket, field) \
                        and field not in no_encript_list:
                    setattr(self.instance, field, key.encrypt(value))
        else:
            for field in self.fields:
                value = self.cleaned_data.get(field)
                if hasattr(self.instance, field) and field not in no_encript_list:
                    setattr(self.instance, field, key.encrypt(value))

        if commit:
            self.instance.save()
        else:
            return self.instance
