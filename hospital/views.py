from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import PatientForm
from .models import Patient


@login_required
def home(request):
    total_patients = Patient.objects.count()

    male_patients = Patient.objects.filter(
        gender__iexact='Male'
    ).count()

    female_patients = Patient.objects.filter(
        gender__iexact='Female'
    ).count()

    return render(
        request,
        'hospital/home.html',
        {
            'total_patients': total_patients,
            'male_patients': male_patients,
            'female_patients': female_patients
        }
    )


@login_required
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = PatientForm()

    return render(
        request,
        'hospital/register_patient.html',
        {'form': form}
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'hospital/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'hospital/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def patient_list(request):
    search = request.GET.get('search')

    if search:
        patients = Patient.objects.filter(
            name__icontains=search
        )
    else:
        patients = Patient.objects.all()

    return render(
        request,
        'hospital/patient_list.html',
        {'patients': patients}
    )


@login_required
def patient_detail(request, id):
    patient = Patient.objects.get(id=id)

    return render(
        request,
        'hospital/patient_detail.html',
        {'patient': patient}
    )


@login_required
def edit_patient(request, id):
    patient = Patient.objects.get(id=id)

    if request.method == 'POST':
        form = PatientForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():
            form.save()
            return redirect('patient_list')

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        'hospital/edit_patient.html',
        {'form': form}
    )


@login_required
def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.delete()

    return redirect('patient_list')