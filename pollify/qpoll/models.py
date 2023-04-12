from django.db import models

class QPoll(models.Model):
  name = models.CharField(max_length=500)
  description = models.CharField(max_length=20_000, blank=True, null=True)
  type = models.CharField(max_length=1000, blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

class Question(models.Model):
  qpoll = models.ForeignKey(QPoll, on_delete=models.CASCADE, related_name='questions')
  title = models.CharField(max_length=2_000)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

class Option(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
  title = models.CharField(max_length=2_000)

  def __str__(self):
      return self.title
