from rest_framework import serializers
from .models import Student, Hobbies, Courses


class HobbiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobbies
        fields = ["hobby_name"]
        
    
class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["course_name"]
        
class StudentSerializer(serializers.ModelSerializer):
    course = CoursesSerializer()
    hobbies = HobbiesSerializer(many=True)
    
    def create(self, data):
        course_data = data.pop('course')  
        hobbies_data = data.pop('hobbies')
        
        course_obj = Courses.objects.get(course_name = course_data['course_name'])
        student = Student.objects.create(course=course_obj, **data)
     
        for each_hobby in hobbies_data:
            hobby_obj = Hobbies.objects.get(hobby_name = each_hobby['hobby_name'])
            student.hobbies.add(hobby_obj)
            
        return student
    
    class Meta:
        model = Student
        exclude = ['updated_at']
        
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    
    def validate(self, data):
        from django.contrib.auth.models import User
        if 'username' in data:
            user = User.objects.filter(username=data["username"])
            if user.exists():
                raise serializers.ValidationError("Username already exists")
            
        if 'email' in data:
            email = User.objects.filter(email=data["email"])
            if email.exists():
                raise serializers.ValidationError("Email already exists")
                
        return data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        if 'username' in data:
            from django.contrib.auth.models import User
            username = User.objects.filter(username=data['username'])
            if not username.exists():
                raise serializers.ValidationError("Username is not exist")
        return data