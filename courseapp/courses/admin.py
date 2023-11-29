from django import forms
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe
from courses import dao

from .models import Category, Course, Lesson, Tag, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'iSuccess'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_course_by_cate()
        })



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Course
        fields = '__all__'

class TagInlineAdmin(admin.StackedInline):
    model = Course.tags.through

class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'subject', 'created_date', 'updated_date', 'category', 'active']
    readonly_fields = ['img']
    inlines = [TagInlineAdmin]
    form = CourseForm

    def img(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                .format(url=course.image.name)
            )
    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }

# Register your models here.
admin_site = CourseAppAdminSite(name='myapp')
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Tag)
# admin.site.register(User)
# admin.site.register(Permission)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson)
# admin.site.register(Tag)
