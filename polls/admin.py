from re import search
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
        ("Close this question", {"fields": ["closed"]}),
        ("Author", {"fields": ["author"]}),
        ("Community", {"fields": ["community"]}),
    ]

    inlines = [ChoiceInline]

    list_display = ("question_text", "pub_date", "closed", "author", "community")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)

# Register your models here.
