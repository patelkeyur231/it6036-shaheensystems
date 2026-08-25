from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Tour, Agent
from .forms import TourForm


def home(request):
    return render(request, 'core/home.html')


class UserLoginView(LoginView):
    template_name = 'core/login.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('login')


@login_required
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'core/tour_list.html', {'tours': tours})


@login_required
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    return render(request, 'core/tour_detail.html', {'tour': tour})


@login_required
def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'core/agent_list.html', {'agents': agents})


@login_required
def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, pk=agent_id)
    return render(request, 'core/agent_detail.html', {'agent': agent})


@login_required
def add_tour(request):
    if not (request.user.groups.filter(name='Managers').exists() or request.user.groups.filter(name='Administrators').exists()):
        return HttpResponseForbidden("You do not have permission to add tours.")

    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm()

    return render(request, 'core/add_tour.html', {'form': form})


@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    is_admin = request.user.groups.filter(name='Administrators').exists()
    is_manager = request.user.groups.filter(name='Managers').exists()
    is_agent = request.user.groups.filter(name='Agents').exists()

    if is_admin or is_manager:
        pass
    elif is_agent:
        if not hasattr(request.user, 'agent') or tour.agent != request.user.agent:
            return HttpResponseForbidden("You can only edit your own tours.")
    else:
        return HttpResponseForbidden("You do not have permission to edit tours.")

    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = TourForm(instance=tour)

    return render(request, 'core/edit_tour.html', {'form': form, 'tour': tour})