# question/models.py
from django.db import models
from usermode.models import CustomUser

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

class CodeSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    test_case_pass = models.BooleanField(default=False)
    no_of_attempt = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submission by {self.user.email} for {self.question.heading}'