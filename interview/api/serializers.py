from rest_framework import serializers

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

    class Meta:
        model = Answer
        fields = (
            'answer_text',
            'answer_choice',
            'answer_multi'
        )

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)