
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('courses', views.CourseViewSet, basename='courses')
# /courses/ - GET
# /courses/ - POST
# /courses/{course_id}/ - GET
# /courses/{course_id}/ - PUT
# /courses/{course_id}/ - DELETE
urlpatterns = [
    path('', include(router.urls)),

]