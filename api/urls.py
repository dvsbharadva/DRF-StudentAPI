from django.urls import path
from .views import StudentView, StudentDetailView, StudentCreateView, StudentUpdateView, RegisterView, StudentDeleteView, LoginView

urlpatterns = [
    path('students/', StudentView.as_view()),
    path('student/<pk>', StudentDetailView.as_view()),
    path('student/create/', StudentCreateView.as_view()),
    path('student/update/', StudentUpdateView.as_view()),
    path('student/register/', RegisterView.as_view()),
    path('student/delete/', StudentDeleteView.as_view()),
    path('student/login/', LoginView.as_view())
] 