from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
import logging

# Modelos importados para la evaluación
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment

logger = logging.getLogger(__name__)

# --- FUNCIÓN AUXILIAR PARA EXTRAER RESPUESTAS ---
def extract_answers(request):
    """
    Busca todas las opciones (choices) seleccionadas en el formulario POST
    cuyos nombres sigan el patrón 'choice_' + id.
    """
    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            choice_id = value
            choice = get_object_or_404(Choice, pk=choice_id)
            selected_choices.append(choice)
    return selected_choices


# --- VISTAS ORIGINALES DEL PROYECTO ---
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'


def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        if not Enrollment.objects.filter(user=request.user, course=course).exists():
            Enrollment.objects.create(user=request.user, course=course)
        return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


# --- VISTAS DE EVALUACIÓN REQUERIDAS (TAREA 5) ---
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    # Obtener el objeto de inscripción asociado
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # Crear un nuevo objeto de presentación (Submission)
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Recoger las opciones utilizando la función auxiliar
    choices = extract_answers(request)
    
    # Guardar las opciones en la relación Many-to-Many
    submission.choices.set(choices)
    submission_id = submission.id
    
    # Redirigir a show_exam_result con el ID de la presentación
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course.id, submission_id,)))


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    total_score = 0
    questions = course.question_set.all()  # Relación inversa de preguntas

    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)  # Respuestas correctas
        selected_choices = choices.filter(question=question)  # Respuestas del alumno

        # Comprobación estricta de conjuntos para validar si la respuesta es 100% correcta
        if set(correct_choices) == set(selected_choices):
            total_score += question.grade  # Suma la calificación si es correcto

    # Variables de contexto obligatorias exigidas por la rúbrica de evaluación
    context['course'] = course
    context['grade'] = total_score
    context['choices'] = choices

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
