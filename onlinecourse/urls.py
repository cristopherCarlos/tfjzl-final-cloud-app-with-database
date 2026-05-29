from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # --- RUTAS EXISTENTES DEL PROYECTO ---
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    
    # --- NUEVAS RUTAS REQUERIDAS (TAREA 5 Y 6) ---
    # Ruta para procesar el envío del formulario del examen (POST)
    path('<int:course_id>/submit/', views.submit, name="submit"),
    
    # Ruta para mostrar la pantalla final de resultados calificados
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="exam_result"),
]
