from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(forms.Form, UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = 'iniciarsesion'
        self.helper.add_input(Submit('registrar', 'Registrar'))


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )


class AddPlayListForm(forms.Form):

    playlist_name = forms.CharField(
        label="Nombre para la playlist",
        max_length=100,
        required=True,
    )

    playlist_description = forms.CharField(
        label="Descripción breve",
        max_length=100,
        required=True,
    )

    playlist_type = forms.TypedChoiceField(
        label="¿Privacidad?",
        choices=((1, "Privada"), (0, "Pública")),
        coerce=lambda x: bool(int(x)),
       # widget=forms.RadioSelect,
        initial='1',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(AddPlayListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-AddPlayListForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'add_playlist'

        self.helper.add_input(Submit('submit', 'Añadir'))
