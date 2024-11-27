import json
from django.http import JsonResponse
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
    ticket = None  # Inicializamos como None en caso de crear un ticket

    # Si se pasa un ticket_id, se obtiene el ticket para editarlo
    if ticket_id:
        ticket = get_object_or_404(Report, id=ticket_id)

    if request.method == "POST":
        form = ReportsForm(request.POST, instance=ticket)  # Usamos el ticket existente si se edita
        if form.is_valid():
            tags = form.cleaned_data.get('tags', [])
            form.instance.tags = tags  # Asignar las etiquetaas al ticket

            # Si estamos editando un ticket existente
            if ticket:
                form.save()
                messages.success(request, "The ticket was updated successfully!")
            else:  # Si estamos creando un ticket nuevo
                form.instance.created_by = user
                form.instance.status = 'WIP'  # Asignamos el estado por defecto como 'WIP'
                form.save()
                messages.success(request, "The ticket was created successfully!")
            return redirect('reports')  # Redirige al listado de tickets

        else:
            messages.error(request, "There was an error processing the form. Please try again.")  # Si hay error en el formulario

    else:
        form = ReportsForm(instance=ticket)  # Si es GET, se carga el formulario vacío o con el ticket a editar

    # Cargar los últimos 2 tickets recientes para mostrar en la vista
    recent_tickets = Report.objects.all().order_by('-created_at')[:2]
    tickets = Report.objects.all()

    return render(request, 'reports/page/reports.html', {
        'form': form,
        'page_title': 'Reports',
        'username': user.username,
        'role': user.role,
        'ticket': ticket,
        'tickets': tickets,
        'recent_tickets': recent_tickets,
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
    
    
@login_required
def get_info_reportes(request):
    user = request.user
    reportes = Report.objects.all()
    low = Report.objects.filter(priority='low').count()
    mid = Report.objects.filter(priority='mid').count()
    high = Report.objects.filter(priority='high').count()
    critical = Report.objects.filter(priority='critical').count()
    bug = sum(1 for report in reportes if 'bug' in report.tags)
    feature = sum(1 for report in reportes if 'feature' in report.tags)
    update = sum(1 for report in reportes if 'update' in report.tags)
    reportes = reportes.count()
    
    data = {
        'reportes': reportes,
        'low': low,
        'mid': mid,
        'high': high,
        'critical': critical,
        'bug': bug,
        'feature': feature,
        'update': update,
    }
    print(data)
    data = JsonResponse(data)
    data['X-Frame-Options'] = 'DENY'
    
    return data