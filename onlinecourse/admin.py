from django.contrib import admin
# Importación de los 7 modelos requeridos por la rúbrica
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# Permitir agregar/editar Lecciones dentro de la vista del Curso
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# Permitir agregar/editar Opciones dentro de la vista de la Pregunta
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

# Permitir agregar/editar Preguntas dentro de otras vistas si es necesario
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# Configuración del panel para Cursos
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# Configuración del panel para Preguntas, incluyendo sus Opciones (ChoiceInline)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content']

# Configuración del panel para Lecciones
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

# Registro formal de todos los modelos en el sitio de administración de Django
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)