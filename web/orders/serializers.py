from web.models import ProductCopy
from web.constans import STAMP_COLORS
from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class ProductCopySerializer(serializers.ModelSerializer):
    color_text = ChoiceField(choices=STAMP_COLORS)
    image = serializers.ImageField(max_length=None,
                                   use_url=True,
                                   allow_null=True,
                                   required=False)

    class Meta:
        model = ProductCopy
        depth = 2
        fields = '__all__'