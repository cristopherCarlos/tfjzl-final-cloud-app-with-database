import sys
from django.utils import timezone
from django.db import models
from django.conf import settings

# --- MODELOS EXISTENTES EN EL PROYECTO ---

class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STUDENT = 'std'
    DEVELOPER = 'dev'
    DATA_SCIENTIST = 'ds'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + self.occupation


class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default="online course")
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=False)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Title: " + self.title


class Enrollment(models.Model):
    AUDIENCE = 'aud'
    LEARNER = 'lrn'
    STATUS_CHOICES = [
        (AUDIENCE, 'Audience'),
        (LEARNER, 'Learner')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)
    mode = models.CharField(max_length=5, choices=STATUS_CHOICES, default=AUDIENCE)
    rating = models.FloatField(default=5.0)


# --- NUEVOS MODELOS AGREGADOS (REQUERIDOS PARA LA EVALUACIÓN) ---

class Question(models.Model):
    # Relación uno a muchos: Un curso tiene muchas preguntas
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Contenido de la pregunta
    content = models.CharField(max_length=500, default="Texto de la pregunta")
    # Calificación o peso de la pregunta
    grade = models.IntegerField(default=10)

    # Método clave para determinar si las respuestas seleccionadas son correctas
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True)
        correct_ids = [answer.id for answer in all_answers]
        return set(correct_ids) == set(selected_ids)

    def __str__(self):
        return "Pregunta: " + self.content


class Choice(models.Model):
    # Relación uno a muchos: Una pregunta tiene muchas opciones
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Contenido de la opción
    content = models.CharField(max_length=500, default="Texto de la opción")
    # Indica si la opción es correcta
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Opción: " + self.content


class Submission(models.Model):
    # Relación uno a muchos: Una inscripción (Enrollment) puede tener múltiples envíos de examen
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    # Relación muchos a muchos: Un envío contiene muchas opciones seleccionadas
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return "Envío de: " + self.enrollment.user.username + " para el curso " + self.enrollment.course.name
