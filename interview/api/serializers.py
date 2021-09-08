from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Category, Question, Choice, Answer, AnswerNumber


class CategoryModelSerializer(ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
        )

    def get_start_date(self, obj):
        print(obj.start_date)
        if obj.start_date:
            return str(obj.start_date)
        else:
            return 'Дата начала не опрeделена'

    def get_end_date(self, obj):
        print(obj.start_date)
        if obj.start_date:
            return str(obj.start_date)
        else:
            return 'Дата окончания не опрeделена'


class QuestionModelSerializer(ModelSerializer):
    type_display = serializers.CharField(source='get_type_display')
    category = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'category',
            'title',
            'type_display',
        ]

    def get_category(self, obj):
        return obj.category.title


class QuestionCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'type'
        ]


class ChoiceModelSerializer(ModelSerializer):
    question = QuestionModelSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ('question', 'title')


class ChoiceCreateSerializer(ModelSerializer):

    class Meta:
        model = Choice
        fields = ('title',)


class AnswerNumberModelSerializer(ModelSerializer):
    class Meta:
        model = AnswerNumber
        fields = []


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class ForChoice(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        qs = Choice.objects.filter(question__id=4)
        return qs


class AnswerModelSerializer(ModelSerializer):
    question = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    # answer_choice = ChoiceModelSerializer
    # answer_multi = ChoiceModelSerializer

    def get_question(self, obj):
        return obj.question.title

    def get_category(self, obj):
        return obj.category.title

    # answer_choice = serializers.PrimaryKeyRelatedField(
    #     # queryset=Choice.objects.filter(question__id=4)
    # )
    #
    # # answer_choice = ForChoice()
    #
    # answer_multi = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     # queryset=Choice.objects.filter(question__id=4)
    # )

    class Meta:
        model = Answer
        fields = (
            'pk',
            'category',
            'question',
            'answer_text',
            'answer_choice',
            'answer_multi',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer_choice'].queryset = Choice.objects.filter(question__id=4)
        self.fields['answer_multi'].queryset = Choice.objects.filter(question__id=4)
