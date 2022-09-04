from django.contrib import admin
from .models import ExamResult, Favourite, MultipleChoiceQuestion, TextQuestion, Topic, TrueFalseQuestion

# Register your models here.

admin.site.register(Topic)
admin.site.register(Favourite)
admin.site.register(ExamResult)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(TextQuestion)