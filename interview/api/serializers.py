from rest_framework import serializers, status
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

    # question = QuestionModelSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = '__all__'


class AnswerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerNumber
        fields = '__all__'
