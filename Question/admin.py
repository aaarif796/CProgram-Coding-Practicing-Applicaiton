# question/admin.py
from django.contrib import admin
from .models import Question, TestCase,CodeSubmission

class TestCaseInline(admin.TabularInline):
    model = TestCase

class QuestionAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
    list_display = ('heading', 'topics', 'level', 'created_at')
    search_fields = ('heading', 'describe', 'topics')
    list_filter = ('level', 'created_at')

admin.site.register(Question, QuestionAdmin)
admin.site.register(CodeSubmission)
