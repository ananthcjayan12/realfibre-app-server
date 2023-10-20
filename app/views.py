from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CustomerForm, MeasurementForm, HingeForm, LockForm, FinishForm, DoorOpenForm, FrameForm, AdvancePaymentForm,DoorForm
from django.http import HttpResponseForbidden
from django.contrib import messages
import json

FRAME_ADJUSTMENTS = {
    'Small': (-7.3, -7.3, -4.3),
    'Normal': (-7.3, -7.3, -4.8),
    'Medium': (-7.3, -7.3, -4.3),
    'Heavy': (-11, -11, -6.3),
    'DoorWithoutClearence': (0, 0, 0),
    'DoorWithClearence': (-0.7, -0.7, -0.8)
}

@login_required
def home(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)  # Temporarily prevent saving
            customer.agent = request.user  # Assign the logged-in user to the agent field
            customer.save()
            return redirect('home')  # Redirect back to the home after saving

    else:
        form = CustomerForm()
        query = request.GET.get('search', '')
        customers = Customer.objects.filter(agent=request.user, name__icontains=query)[:5]  # Added search functionality and limited to first 5

    return render(request, 'home.html', {'customers': customers, 'form': form})



def door_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    doors = Door.objects.filter(customer=customer).order_by('id')
    
    if request.method == "POST":
        # Logic to create a new door
        new_door = Door(customer=customer)
        new_door.save()
        # Redirect to the door selection page again to see the updated list
        return redirect('door_selection', customer_id=customer_id)
    
    context = {
        'customer': customer,
        'doors': doors,
    }
    
    return render(request, 'select_door.html', context)

def delete_door(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    customer_id = door.customer.id
    door.delete()
    return redirect('door_selection', customer_id=customer_id)

def door_process(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    
    # If you want to process anything, you'll handle it here. Otherwise:
    return render(request, 'door_process.html', {'door': door})



@login_required
def process_selection(request, door_id):
    doors = get_object_or_404(Door, id=door_id)
    return render(request, 'process_selection.html', {'doors': doors})

@login_required
def measurement(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    existing_measurement = door.measurement
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=existing_measurement)
        if form.is_valid():
            measurement = form.save(commit=False)
            door.measurement = measurement
            measurement.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = MeasurementForm(instance=existing_measurement)
        print(form.instance)

    return render(request, 'measurement.html', {'door': door, 'form': form})

@login_required
def select_hinge(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    hinge_instance = door.hinge_selection

    if request.method == 'POST':
        form = HingeForm(request.POST, instance=hinge_instance)
        if form.is_valid():
            hinge = form.save(commit=False)
            door.hinge_selection = hinge
            hinge.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = HingeForm(instance=hinge_instance)

    return render(request, 'select_hinge.html', {'door': door, 'form': form})


@login_required
def lock_selection(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    lock_instance = door.lock_selection

    if request.method == "POST":
        form = LockForm(request.POST, instance=lock_instance)
        if form.is_valid():
            lock_obj = form.save(commit=False)
            door.lock_selection = lock_obj
            lock_obj.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = LockForm(instance=lock_instance)

    return render(request, 'lock_selection.html', {'door': door, 'form': form})

@login_required
def finish_selection(request, customer_id, door_id):
    customer = get_object_or_404(Customer, id=customer_id)
    door = get_object_or_404(Door, id=door_id)
    existing_finish = Finish.objects.filter(door=door).first()

    if request.method == "POST":
        form = FinishForm(request.POST, instance=existing_finish)
        if form.is_valid():
            finish_instance = form.save(commit=False)
            finish_instance.door = door
            finish_instance.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        form = FinishForm(instance=existing_finish)

    return render(request, 'finish_selection.html', {'customer': customer, 'door': door, 'form': form})



@login_required
def update_advance_payment(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = AdvancePaymentForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        form = AdvancePaymentForm(instance=customer)

    return render(request, 'update_advance_payment.html', {'form': form, 'customer': customer})

@login_required
def door_open_selection(request, customer_id, door_id):
    customer = get_object_or_404(Customer, id=customer_id)
    door = get_object_or_404(Door, id=door_id)
    existing_door_open = DoorOpen.objects.filter(door=door).first()  # Assuming DoorOpen model exists

    if request.method == "POST":
        form = DoorOpenForm(request.POST, instance=existing_door_open)
        if form.is_valid():
            door_open_instance = form.save(commit=False)
            door_open_instance.door = door
            door_open_instance.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        form = DoorOpenForm(instance=existing_door_open)

    return render(request, 'door_open_selection.html', {'customer': customer, 'door': door, 'form': form})


@login_required
def frame_selection(request, customer_id, door_id):
    customer = get_object_or_404(Customer, id=customer_id)
    door = get_object_or_404(Door, id=door_id)
    existing_frame = Frame.objects.filter(door=door).first()  # Assuming Frame model exists

    if request.method == "POST":
        form = FrameForm(request.POST, instance=existing_frame)
        if form.is_valid():
            frame_instance = form.save(commit=False)
            frame_instance.door = door
            frame_instance.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        form = FrameForm(instance=existing_frame)

    return render(request, 'frame_selection.html', {'customer': customer, 'door': door, 'form': form})
