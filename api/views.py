from django.shortcuts import render
from django.http import request, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentSerializer, HobbiesSerializer, CoursesSerializer, RegisterSerializer, LoginSerializer
from .models import Student, Hobbies, Courses
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .permission import ValidStudentPermission
# Create your views here.


class StudentView(APIView):
    def get(self, request):
        try:
            students = Student.objects.all()
            if request.GET.get('search'):
                search = request.GET.get('search')
                students = students.filter(
                    Q(name__icontains = search) |
                    Q(mobile__iexact = search) 
                )
            serializer = StudentSerializer(students, many = True)
                
            return Response({
                'status': True,
                'message': "All students are fetched",
                "data" : serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': f'Error: {str(e)}',
                'data' : {}
            })
    
class StudentDetailView(APIView):
    def get(self, request, pk):
        data = request.data
        try:
            student = Student.objects.get(id=pk)
            serializer = StudentSerializer(student)
            return Response({
                'status': True,
                'message': 'Student deatils view',
                'data':serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': f'Error: {str(e)}',
                'data' : {}
            })
            
class StudentCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ValidStudentPermission]
    def post(self, request):
        data = request.data            
        serializer = StudentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message' : 'Student created successfully!',
                'data' : serializer.data
            })
        return Response({
            'status' : False,
            'message' : 'Data is not valid',
            'data' : serializer.errors
        })

class StudentUpdateView(APIView):        
    def patch(self, request):
        try:
            data = request.data
            if data.get('id') is None:
                return Response({
                    'status': False,
                    'message' : "Id is required",
                    "data" : {}
                })
                
            student_obj = Student.objects.filter(id=data.get('id'))
            if not student_obj.exists():
                return Response({
                    'status' : False,
                    'message' : 'Id is not valid',
                    'data' : {}
                })
                
            print("Student obj[0] : ", student_obj[0], "Student obj : ", student_obj, "\n data from views.py: ", data)
            student_obj = student_obj[0]
        
            serializer = StudentSerializer(student_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message' : 'Data updated successfully!',
                    'data' : serializer.data
                })
            return Response({
                'status' : False,
                'message' : 'Data is not valid',
                'data' : serializer.errors
            })
        except Exception as e:
            return Response({
                'status' : False,
                'message' : f'Error: {str(e)}',
                'data' : {}
            })

class StudentDeleteView(APIView):
    def delete(self, request):
        try:
            if request.data.get('id') is None:
                return Response({
                    'status': False,
                    'message' : 'Student ID is required',
                    'data' : {}
                })            
            
            student = Student.objects.filter(id=request.data.get('id'))
            # student = student[0]
            if not student.exists():
                return Response({
                    'status': False,
                    'message' : 'Student ID is not found',
                    'data' : {}
                })
            # student_name = student.name()    
            student.delete()
            return Response({
                'status': True,
                'message' : f'Student is deleted',
                'data' : {}
            })
        except Exception as e:
            return Response({
                    'status': False,
                    'message' : f'something is wrong: {str(e)}',
                    'data' : {}
                })
class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            # serializer = Regi
            serializer = RegisterSerializer(data = data)
            if serializer.is_valid():
                # serializer.save()
                from django.contrib.auth.models import User
                student = User.objects.create(
                    username = serializer.data['username'],
                    email = serializer.data['email']
                )
                student.set_password(serializer.data['password'])
                student.save()
                return Response({
                    'status' : True,
                    'message': 'New user registered successfully',
                    'data' : serializer.data
                })
            return Response({
                'status' : False,
                'message' : 'Data is not valid',
                'data' : serializer.errors
            })
        except Exception as e:
            return Response({
                'status' : False,
                'message' : f'Error: {str(e)}',
                'data' : {}
            })
            
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        try:
            if serializer.is_valid():
                user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
                
                if user:
                    token =Token.objects.get_or_create(user=user)
                    return Response({
                        'status' : True,
                        'message': 'You\'re logged in successfully ',
                        'data' : {
                            'token': f'{str(token[0])}'
                        }
                    })
                    
                return Response({
                    'status' : False,
                    'message': 'Password is incorrect',
                    'data' : {}
                })
            
            return Response({
                'status' : False,
                'message': 'Validation error',
                'data' : serializer.errors
            })
        
        except Exception as e:
            return Response({
                'status' : False,
                'message': f'Something went wrong : {str(e)}',
                'data' : {}
            })
        
        
        