from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import (
    User,
    Student,
    Parent,
    Teacher,
    Admin,
    Course,
    Grade,
    Attendance,
    Announcement,
)

# Get the custom User model
User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff", "role")
    list_filter = ("is_staff", "is_superuser", "is_active", "role")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    def delete_model(self, request, obj):
        """Custom delete to handle multi-table inheritance"""
        if hasattr(obj, "student"):
            obj.student.delete()
        elif hasattr(obj, "parent"):
            obj.parent.delete()
        elif hasattr(obj, "teacher"):
            obj.teacher.delete()
        elif hasattr(obj, "admin"):
            obj.admin.delete()
        super().delete_model(request, obj)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "grade_level",
        "guardian",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("grade_level",)


class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "role", "phone_number")
    search_fields = ("email", "first_name", "last_name")


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "role", "department")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("department",)


class AdminAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "role", "office_number")
    search_fields = ("email", "first_name", "last_name")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    search_fields = ("name",)
    list_filter = ("name", "teacher")


class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "exam_type", "score")
    list_filter = ("course", "exam_type")
    search_fields = ("student__email", "course__name")


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "is_present")
    list_filter = ("course", "date", "is_present")
    search_fields = ("student__email", "course__name")


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("content", "date_posted")
    search_fields = ("content",)
    list_filter = ("date_posted",)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
