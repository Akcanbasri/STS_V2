from rest_framework import serializers
from django.contrib.auth.hashers import make_password
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

# Get the User model
User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
            "is_active",
            "is_staff",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        # Set users to inactive if you want them to verify their email or be approved
        validated_data["is_active"] = True
        return super().create(validated_data)


# Admin Creation Serializer
class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "office_number",
            "is_active",
            "is_staff",
            "role",
        ]

    def create(self, validated_data):
        validated_data["role"] = "admin"
        validated_data["is_staff"] = True  # Typically admins are staff
        validated_data["password"] = make_password(validated_data["password"])
        return Admin.objects.create(**validated_data)


# Teacher Creation Serializer
class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "department",
            "is_active",
            "is_staff",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return Teacher.objects.create(**validated_data)


# Parent Creation Serializer
class ParentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "phone_number",
            "is_active",
            "is_staff",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return Parent.objects.create(**validated_data)


# Student Creation Serializer
class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "grade_level",
            "guardian",
            "is_active",
            "is_staff",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return Student.objects.create(**validated_data)


# General User Serializer for reading user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "role",
        ]


# Serializers for Course, Grade, Attendance, and Announcement models
class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherCreateSerializer(read_only=True)
    students = StudentCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "teacher", "students"]


class GradeSerializer(serializers.ModelSerializer):
    student = StudentCreateSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "student", "course", "exam_type", "score"]


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentCreateSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student", "course", "date", "is_present"]


class AnnouncementSerializer(serializers.ModelSerializer):
    target_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = ["id", "content", "date_posted", "target_users"]
