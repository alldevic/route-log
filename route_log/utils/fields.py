from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return {
            'id': value,
            'name': self._get_choices().get(value, None)
        }


class PhotoField(serializers.FileField):
    """
    Attachements relation
    """
    def to_representation(self, value):
        if value.last():
            return value.last().file.url
