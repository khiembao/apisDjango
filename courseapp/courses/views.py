from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.decorators import action
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.response import Response

from courses import serializers, paginaters
from .models import Course, Category, Lesson, User, Comment




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

class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True).all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, lesson=self.get_object(), content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]
    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)



# def index(request):
#     return render(request, template_name='index.html', context={
#         'name': 'Bao Khiem'
#     })
