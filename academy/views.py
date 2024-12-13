from django.shortcuts import redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Certification, Course, UserProfile
from .forms import CourseForm, UserAvatarForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Q

class CourseListView(ListView):
    model = Course
    template_name = 'academy/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        queryset = Course.objects.all()
        
        # Get search query from URL parameters
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')

        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search query to context to maintain it in the search input
        context['search_query'] = self.request.GET.get('search', '')
        # Add categories for the filter
        context['categories'] = Course.objects.values_list('category', flat=True).distinct()
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'academy/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_courses'] = Course.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'academy/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'academy/course_form.html'

    def test_func(self):
        course = self.get_object()
        return self.request.user.is_staff

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
    template_name = 'academy/course_confirm_delete.html'

    def test_func(self):
        course = self.get_object()
        return self.request.user.is_staff

def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.is_authenticated:
        course.students.add(request.user)
        return redirect('my_courses')
    return redirect('login')

class CertificationListView(ListView):
    model = Certification
    template_name = 'academy/certification_list.html'
    context_object_name = 'certifications'
    paginate_by = 9

    def get_queryset(self):
        queryset = Certification.objects.all()
        
        # Get search query from URL parameters
        search_query = self.request.GET.get('search')
        level = self.request.GET.get('level')

        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(level__icontains=search_query)
            )
        
        if level:
            queryset = queryset.filter(level=level)
            
        return queryset.order_by('level', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search query to context to maintain it in the search input
        context['search_query'] = self.request.GET.get('search', '')
        # Add levels for the filter
        context['levels'] = Certification.objects.values_list('level', flat=True).distinct()
        return context
    
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    next_page = 'profile'  # Add this line

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Il y a eu une erreur lors de la création de votre compte. Veuillez réessayer.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrolled_courses'] = Course.objects.filter(students=self.request.user)
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'auth/profile_edit.html'
    success_url = reverse_lazy('profile')
    form_class = UserProfileForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create profile if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        
        if self.request.POST:
            context['avatar_form'] = UserAvatarForm(
                self.request.POST, 
                self.request.FILES, 
                instance=profile
            )
        else:
            context['avatar_form'] = UserAvatarForm(instance=profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        avatar_form = context['avatar_form']
        
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_form.save()
            messages.success(self.request, "Votre profil a été mis à jour avec succès.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, "Une erreur est survenue lors de la mise à jour de votre profil.")
        return super().form_invalid(form)
    
    
class MyCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'academy/my_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user)