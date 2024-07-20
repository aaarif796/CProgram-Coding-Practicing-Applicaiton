# question/models.py
from django.db import models

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=255)
    describe = models.TextField()
    topics = models.CharField(max_length=255)
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

class TestCase(models.Model):
    question = models.ForeignKey(Question, related_name='test_cases', on_delete=models.CASCADE)
    test_data = models.TextField()

    def __str__(self):
        return f'TestCase for {self.question.heading}'
