from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('crear-nota/', views.crear_nota, name='crear_nota'),
    path('crear-tarea/', views.crear_tarea, name='crear_tarea'),
    path('crear-presupuesto/', views.crear_presupuesto, name='crear_presupuesto'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('editar-categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar-categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('editar-nota/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('eliminar-nota/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('editar-tarea/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar-tarea/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('marcar-tarea-completada/<int:tarea_id>/', views.marcar_tarea_completada, name='marcar_tarea_completada'),
    path('editar-presupuesto/<int:presupuesto_id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('eliminar-presupuesto/<int:presupuesto_id>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
    path('exportar-csv/', views.exportar_csv, name='exportar_csv'),
]
