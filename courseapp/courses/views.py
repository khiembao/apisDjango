from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.decorators import action
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import Course, Category, Lesson
from courses import serializers, paginaters



# Create your views here.
# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.filter(active=True)
#     serializer_class = CourseSerializer
#     # detail -->  xem chi tiet 1 khoa hoc
#     # list (GET) --> xem danh sach khoa hoc
#     # ... (POST) --> them khoa hoc
#     # ... (PUT) --> cap nhat
#     # ... (DELETE) --> xoa khoa hoc
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True).all()
    serializer_class = serializers.CourseSerializer
    pagination_class = paginaters.CoursePaginator

    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(subject__icontains=q)
        return queries
    @action(methods=['get'], detail=True)
    def lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True).all()

        return Response(serializers.LessonSerializer(lessons, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


def index(request):
    return render(request, template_name='index.html', context={
        'name': 'Bao Khiem'
    })
