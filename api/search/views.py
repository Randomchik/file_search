from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Search
from .serializers import SearchCreateSerializer, SearchResultSerializer
from .tasks import start_search_thread


schema_view = get_schema_view(
    openapi.Info(
        title="Search File swagger",
        default_version='1.0.0',
        description="",
    ),
    public=True
)

class CreateSearchView(APIView):
    def post(self, request):
        serializer = SearchCreateSerializer(data=request.data)
        if serializer.is_valid():
            search = serializer.save()
            start_search_thread(search.id)  # Фоновый запуск поиска
            return Response({"search_id": str(search.id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSearchResultsView(APIView):
    def get(self, _, search_id):
        try:
            search = Search.objects.get(id=search_id)
            serializer = SearchResultSerializer(search)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Search.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
