from django.urls import path
from . import views


urlpatterns = [
    path('', views.raiz, name='raiz'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentation/', views.documentation, name='documentation'),
    path('reports/', views.reports, name='reports'),  # Vista de creación de tickets
    path('reports/<int:ticket_id>/', views.reports, name='modify_ticket'),  # Vista de modificación de tickets
    path('logout/', views.logout_request, name='logout'),
    path("registro/", views.registro, name="registro"),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('settings/',views.settings,name='settings'),
    path('notifications/',views.notifications,name='notifications'),
]


