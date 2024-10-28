from rest_framework import serializers

from .models import Search

class SearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['text', 'file_mask', 'size_value', 'size_operator', 'creation_time_value', 'creation_time_operator']
        
class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['finished', 'results']
