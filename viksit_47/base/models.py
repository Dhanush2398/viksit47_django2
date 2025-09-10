from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20)
    gmail = models.EmailField()
    district_name = models.CharField(max_length=100)
    taluk_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
    
class Course(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Online & Offline'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='both')
    price_online = models.PositiveIntegerField(default=2000)
    price_offline = models.PositiveIntegerField(default=2500)

    def __str__(self):
        return self.title

class Mock(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="mocks")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="mock_tests/", blank=True, null=True)
    time_limit = models.PositiveIntegerField(default=30)
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    def __str__(self):
       
        return f"{self.course.title} - {self.title} ({self.get_difficulty_display()})"

class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="study_materials")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="study_materials/", blank=True, null=True)


    
class Question(models.Model):
    mock = models.ForeignKey(Mock, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to="mock_questions/", blank=True, null=True)

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"


class MockResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mock = models.ForeignKey("Mock", on_delete=models.CASCADE)
    
    total = models.IntegerField(default=0)       
    attempted = models.IntegerField(default=0)  
    correct = models.IntegerField(default=0)     
    score = models.FloatField(default=0)       
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.total > 0:
            self.score = (self.correct / self.total) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.mock.title} ({self.score:.2f}%)"
  


class StudyMaterialItem(models.Model):
    study_material = models.ForeignKey(
        StudyMaterial, related_name="items", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="study_material_items/", blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.study_material.title})"


class Author(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    education = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors/')

    def __str__(self):
        return f"{self.name} ({self.course.title})"

class CourseSubscription(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline + Website Access'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')  
    end_date = models.DateField()
    uu_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.get_mode_display()})"
