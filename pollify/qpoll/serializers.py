from rest_framework import serializers
from .models import *
from django.db import transaction

class OptionSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False)

  class Meta:
    model = Option
    fields = ['id', 'title']
    ordering = ['id']


class QuestionSerializer(serializers.ModelSerializer):
  options = OptionSerializer(many=True)
  id = serializers.IntegerField(required=False)

  class Meta:
    model = Question
    fields = ['id', 'title', 'options', 'created', 'updated']
    ordering = ['id']

class QPollSerializer(serializers.ModelSerializer):
  questions = QuestionSerializer(many=True)

  class Meta:
    model = QPoll
    fields = ['id', 'name', 'description', 'type', 'questions', 'created', 'updated']
    ordering = ['id']

  @transaction.atomic
  def create(self, validated_data):
    questions_data = validated_data.pop('questions', [])
    qpoll = QPoll.objects.create(**validated_data)

    self.update_questions(isinstance, questions_data)

    return qpoll

  @transaction.atomic
  def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.description = validated_data.get('description', instance.description)
    instance.save()

    # Update the nested questions
    questions_data = validated_data.get('questions', [])

    self.update_questions(instance, questions_data)

    return instance

  def update_questions(self, instance, questions_data):
    question_ids_in_params = []
    question_ids_in_db = list(instance.questions.values_list('id', flat=True))

    for question_data in questions_data:
      question_id = question_data.pop('id', None)
      question_ids_in_params.append(question_id)
      options_data = question_data.pop('options', [])

      if question_id:
        try:
          question = Question.objects.get(id=question_id, qpoll=instance)
          question.title = question_data.get('title', question.title)
          question.save()
        except Question.DoesNotExist:
          question = Question.objects.create(qpoll=instance, **question_data)
      else:
        question = Question.objects.create(qpoll=instance, **question_data)

      self.update_options(question, options_data)

    question_ids_to_delete = [item for item in question_ids_in_db if item not in question_ids_in_params]

    entries_to_delete = Question.objects.filter(id__in=question_ids_to_delete)
    deleted_count, _ = entries_to_delete.delete()

    return instance


  def update_options(self, question, options_data):
    option_ids_in_params = []
    option_ids_in_db = list(question.options.values_list('id', flat=True))

    for option_data in options_data:
      option_id = option_data.pop('id', None)
      option_ids_in_params.append(option_id)

      if option_id:
        try:
          option = Option.objects.get(id=option_id, question=question)
          option.title = option_data.get('title', option.title)
          option.save()
        except Option.DoesNotExist:
          Option.objects.create(question=question, **option_data)
      else:
        Option.objects.create(question=question, **option_data)

    option_ids_to_delete = [item for item in option_ids_in_db if item not in option_ids_in_params]

    entries_to_delete = Option.objects.filter(id__in=option_ids_to_delete)
    deleted_count, _ = entries_to_delete.delete()

    return question
