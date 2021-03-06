import datetime

from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=400)
    thumbs_up = models.IntegerField(default=0)
    thumps_down = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse('polls:results', kwargs={'pk': self.question.pk})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    class Meta:
        ordering = ['-votes']