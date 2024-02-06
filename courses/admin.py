from django.contrib import admin
from courses.models import Program, Course, Module


@admin.register(Program)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'program', 'created_at']
    list_filter = ['created_at', 'program']
    search_fields = ['title', 'review']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
