from django.db import models
import uuid
# Create your models here

class StudentBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract : True
    
class Courses(StudentBase):
    course_name = models.CharField("Enter Course", max_length=50)
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['course_name']
    
    def __str__(self):
        return self.course_name
    
class Hobbies(StudentBase):
    hobby_name = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Hobby"
        verbose_name_plural = "Hobbies"
        ordering = ['hobby_name']
    
    def __str__(self) -> str:
        return self.hobby_name
    
class Student(StudentBase):

    name = models.CharField(max_length=16)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="student_stream")
    address = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True)
    hobbies = models.ManyToManyField(Hobbies)
        
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['name']

    def __str__(self):
        return self.name
