from django import forms
from .models import UserApp  # Importa tu modelo personalizado
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Report
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login


class ReportsForm(forms.ModelForm):
    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('update', 'Update'),
    ]

    tags = forms.MultipleChoiceField(
        choices=TAG_CHOICES,  # Opciones para los tags
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
    )

    class Meta:
        model = Report
        fields = [
            'title',
            'created_by',
            'assigned_to',
            'affected_product',
            'description',
            'priority',
            'tags',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ticket title'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'affected_product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide a detailed description'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preseleccionar los tags si el formulario está vinculado a una instancia
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags



# Formulario para el registro de usuario
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserApp  # Cambiar de User a UserApp
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Formulario de login
class LoginForm(LoginView):
    template_name = 'auth/login.html'

    # Aquí puedes personalizar el formulario de login si lo necesitas
    # Si usas el formulario por defecto de Django, no es necesario cambiar nada.


# Formulario de logout
class LogoutForm(LogoutView):
    template_name = 'auth/logout.html'


# Formulario para la edición del perfil de usuario
class EditProfile(UserChangeForm):
    nombre = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    

    class Meta:
        model = UserApp  # Cambiar de User a UserApp
        fields = ('nombre','username', 'email', 'password')


class CustomEditProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Nueva contraseña",
        help_text="Deja este campo vacío si no deseas cambiar la contraseña."
    )

    class Meta:
        model = UserApp
        exclude = [
            'last_login', 
            'groups', 
            'user_permissions', 
            'status', 
            'is_active',
            'is_superuser',  # Excluir el campo superuserstatus
            'is_staff',  # Excluir el campo staff status
            'role'  # Excluir el campo role
        ]
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Asegurarnos de obtener el request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)

        # Solo cambiar la contraseña si el campo no está vacío
        new_password = self.cleaned_data.get('password')
        if new_password:  # Solo si hay una nueva contraseña
            user.password = make_password(new_password)

        # Protege los campos sensibles (se restauran al valor actual en la base de datos)
        if user.pk:  # Asegura que el usuario ya existe
            original_user = self._meta.model.objects.get(pk=user.pk)
            
            # Restaurar valores simples
            for field in ['last_login', 'status', 'is_active']:
                if hasattr(user, field):
                    setattr(user, field, getattr(original_user, field))
            
            # Restaurar relaciones many-to-many
            user.groups.set(original_user.groups.all())
            user.user_permissions.set(original_user.user_permissions.all())

        if commit:
            user.save()
            # Guardar relaciones many-to-many después de guardar el objeto principal
            self.save_m2m()

            # Si la contraseña se cambió, iniciar sesión nuevamente
            if new_password and self.request:
                from django.contrib.auth import login
                login(self.request, user)

        return user