from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from .serializers import (
    StudentCreateSerializer,
    TeacherCreateSerializer,
    ParentCreateSerializer,
    AdminCreateSerializer,
)
from .models import Student, Teacher, Parent, Admin
from .permissions import IsAdminUser


class StudentCreateViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [IsAdminUser]


class TeacherCreateViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherCreateSerializer
    permission_classes = [IsAdminUser]


class ParentCreateViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentCreateSerializer
    permission_classes = [IsAdminUser]


class AdminCreateViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminCreateSerializer
    permission_classes = [IsAdminUser]
