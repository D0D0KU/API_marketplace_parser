from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    data_to_parse = serializers.CharField(max_length=1000)


class LinksSerializer(serializers.Serializer):
    links = serializers.ListField(child=serializers.URLField())