from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm, EditProfile,ReportsForm,CustomEditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import UserApp, Report  # Asegúrate de importar tu modelo UserApp
from django.contrib.auth import update_session_auth_hash

def raiz(request):
    return render(request, 'raiz.html')

@login_required
def dashboard(request):
    user = request.user
    return render(request, 'dashboard/dashboard.html',{
        'page_title':'Dashboard',
        'username':user.username,
        'role':user.role,
    })

@login_required
def documentation(request):
    user = request.user
    return render(request, 'documentation.html',{
        'page_title':'Documentation',
        'username':user.username,
        'role':user.role,
    })

@login_required
def reports(request, ticket_id=None):
    user = request.user
    ticket = None

    # Si hay un ticket_id, estamos editando un ticket existente
    if ticket_id:
        ticket = get_object_or_404(Report, id=ticket_id)

    if request.method == "POST":
        # Vincula el formulario a la instancia del ticket (si existe)
        form = ReportsForm(request.POST, instance=ticket)
        if form.is_valid():
            # Guardar los tags correctamente
            tags = form.cleaned_data.get('tags', [])
            form.instance.tags = tags  # Guardar los tags como lista

            # Determinar si se está modificando o creando
            if ticket:  # Modificando
                form.save()
                messages.success(request, "The ticket was updated successfully!")
            else:  # Creando uno nuevo
                form.instance.created_by = user
                form.save()
                messages.success(request, "The ticket was created successfully!")
            return redirect('reports')  # Redirigir después de guardar
        else:
            messages.error(request, "There was an error processing the form. Please try again.")
    else:
        # Si es una solicitud GET, prepara el formulario con la instancia correspondiente
        form = ReportsForm(instance=ticket)

    # Obtener los 2 tickets más recientes
    recent_tickets = Report.objects.all().order_by('-created_at')[:2]  # Asumiendo que 'created_at' es el campo de fecha de creación
    tickets = Report.objects.all()  # Obtener todos los tickets

    return render(request, 'reports/page/reports.html', {
        'form': form,
        'page_title': 'Reports',
        'username': user.username,
        'role': user.role,
        'ticket': ticket,
        'tickets': tickets,
        'recent_tickets': recent_tickets,  # Pasa los tickets recientes al template
    })



@login_required
def notifications(request):
    user = request.user
    return render(request, 'notifications.html',{
        'page_title':'Notifications',
        'username':user.username,
        'role':user.role,
    })

def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardamos el usuario creado
            login(request, user)  # Iniciar sesión automáticamente
            messages.success(request, 'Tu cuenta ha sido creada exitosamente. ¡Ahora estás logueado!')
            return redirect('dashboard')  # Redirigir al dashboard o donde lo necesites
    else:
        form = UserRegisterForm()
    return render(request, "auth/registro.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("raiz")


@login_required
def settings(request):
    user = request.user

    if request.method == 'POST':
        form = CustomEditProfileForm(request.POST, instance=user, request=request)  # Pasar el request aquí
        if form.is_valid():
            form.save()  # El formulario se guarda
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('settings')  # Redirigir después de guardar los cambios
    else:
        form = CustomEditProfileForm(instance=user, request=request)  # Pasar el request aquí también

    return render(request, 'settings.html', {
        'form': form,
        'page_title':'Settings',
        'username':user.username,
        'role':user.role,
        'form':form
    })

    
    
    


    
