from rest_framework import serializers
from .models import Search

class SizeSerializer(serializers.Serializer):
    value = serializers.IntegerField(required=False, allow_null=True)
    operator = serializers.CharField(max_length=2, required=False, allow_null=True)

class CreationTimeSerializer(serializers.Serializer):
    value = serializers.DateTimeField(required=False, allow_null=True)
    operator = serializers.CharField(max_length=2, required=False, allow_null=True)

class SearchCreateSerializer(serializers.ModelSerializer):
    size = SizeSerializer(required=False)
    creation_time = CreationTimeSerializer(required=False)
    
    class Meta:
        model = Search
        fields = ['text', 'file_mask', 'size', 'creation_time']

    def create(self, validated_data):
        size_data = validated_data.pop('size', None)
        creation_time_data = validated_data.pop('creation_time', None)
        
        search = Search.objects.create(**validated_data)
        
        if size_data and size_data['value'] and size_data['value']:
            search.size_value = size_data['value']
            search.size_operator = size_data['operator']
        
        if creation_time_data and creation_time_data['value'] and creation_time_data['operator']:
            search.creation_time_value = creation_time_data['value']
            search.creation_time_operator = creation_time_data['operator']
        
        search.save()
        return search

class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['finished', 'results']
