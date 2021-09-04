from rest_framework import serializers, status
from rest_framework.fields import empty, UUIDField
from rest_framework.response import Response

from ..models import Category, Question, Choice, Answer, AnswerNumber


class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('owner',)


class QuestionModelSerializer(serializers.ModelSerializer):

    type_display = serializers.CharField(source='get_type_display')

    class Meta:
        model = Question
        fields = [
            'id',
            'category',
            'title',
            'type_display'
        ]


class QuestionCreateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            'id',
            # 'category',
            'title',
            'type'
        ]


class QuestionModelSerializer(serializers.ModelSerializer):

    type_display = serializers.CharField(source='get_type_display')

    class Meta:
        model = Question
        fields = [
            'id',
            'category',
            'title',
            'type_display'
        ]




class ChoiceModelSerializer(serializers.ModelSerializer):

    question = QuestionModelSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ('question', 'title')


class AnswerNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerNumber
        fields = []


class AnswerModelSerializer(serializers.ModelSerializer):

    answer_choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = Answer
        fields = (
            'answer_text',
            'answer_choice',
            'answer_multi'
        )

    def create(self, validated_data):
        question_id = validated_data.get('question', None)
        if question_id is not None:
            question = Question.objects.filter(id=question_id).first()
            if question is not None:
                answer_choice = question.answer
                if answer_choice is not None:
                   # update your answer
                   return answer_choice

        answer_choice = Answer.objects.create(**validated_data)
        return answer_choice
