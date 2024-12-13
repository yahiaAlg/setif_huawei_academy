from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('courses/', views.CourseListView.as_view(), name='courses'),  # Added this line
    path('certifications/', views.CertificationListView.as_view(), name='certifications'),  # Added this line
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/new/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('course/<int:pk>/enroll/', views.enroll_course, name='course_enroll'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='course_list'), name='logout'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    
    # Profile URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('my-courses/', views.MyCoursesView.as_view(), name='my_courses'),  # Add this line
]