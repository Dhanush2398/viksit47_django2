from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ( Profile, CourseSubscription, Mock, Question, Option,Author, StudyMaterial, StudyMaterialItem, Course
)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

class CourseSubscriptionInline(admin.TabularInline):
    model = CourseSubscription
    extra = 0
    readonly_fields = ("amount", "is_paid", "end_date", "transaction_id")
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, CourseSubscriptionInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_mock', 'get_course')
    inlines = [OptionInline]
    search_fields = ('text',)

    def get_mock(self, obj):
        return obj.mock.title
    get_mock.short_description = 'Mock'

    def get_course(self, obj):
        return obj.mock.course.title
    get_course.short_description = 'Course'

class MockAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'difficulty', 'time_limit')
    list_filter = ('course', 'difficulty')
    search_fields = ('title',)


class StudyMaterialItemInline(admin.TabularInline):
    model = StudyMaterialItem
    extra = 1


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [StudyMaterialItemInline]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'education')  
    search_fields = ('name', 'course__title')
    list_filter = ('course',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "mode", "price_online", "price_offline")
    search_fields = ("title",)


admin.site.register(Mock, MockAdmin)
admin.site.register(Question, QuestionAdmin)
