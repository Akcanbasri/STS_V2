from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    need_password_change = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=30,
        choices=[
            ("student", "Student"),
            ("parent", "Parent"),
            ("teacher", "Teacher"),
            ("admin", "Admin"),
        ],
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Student(User):
    grade_level = models.CharField(max_length=10)
    guardian = models.ForeignKey(
        "Parent", on_delete=models.CASCADE, related_name="children"
    )


class Parent(User):
    phone_number = models.CharField(max_length=15)


class Teacher(User):
    department = models.CharField(max_length=100)


class Admin(User):
    office_number = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.role = "admin"  # Ensure the role is set correctly
        super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="courses_taught"
    )
    students = models.ManyToManyField(Student, related_name="courses_enrolled")


class Grade(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    exam_type = models.CharField(max_length=100)
    score = models.FloatField()


class Attendance(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendance_records"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="attendance_records"
    )
    date = models.DateField()
    is_present = models.BooleanField()


class Announcement(models.Model):
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    target_users = models.ManyToManyField(User, related_name="announcements")
