from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm ,MeasurementForm,FinishForm,DoorOpenForm,AdvancePaymentForm
from .models import Measurement,Hinge,Finish,DoorOpen
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

@login_required
def process_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'process_selection.html', {'customer': customer})


from .forms import MeasurementForm

@login_required
def measurement(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    try:
        existing_measurement = Measurement.objects.get(customer=customer)
    except Measurement.DoesNotExist:
        existing_measurement = None

    if request.method == 'POST':
        if existing_measurement:
            form = MeasurementForm(request.POST, instance=existing_measurement)
        else:
            form = MeasurementForm(request.POST)
        
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.customer = customer
            measurement.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        if existing_measurement:
            form = MeasurementForm(instance=existing_measurement)
        else:
            form = MeasurementForm()

    return render(request, 'measurement.html', {'customer': customer, 'form': form})

from .forms import HingeForm

@login_required
def select_hinge(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Ensure the customer belongs to the logged-in agent
    if customer.agent != request.user:
        return HttpResponseForbidden("You don't have permission to access this page.")

    hinge_instance, created = Hinge.objects.get_or_create(customer=customer)

    if request.method == 'POST':
        form = HingeForm(request.POST, instance=hinge_instance)
        if form.is_valid():
            hinge = form.save()  # The instance is automatically saved or updated
            return redirect('process_selection', customer_id=customer.id)

    else:
        form = HingeForm(instance=hinge_instance)

    return render(request, 'select_hinge.html', {'customer': customer, 'form': form, 'hinge': hinge_instance})

from django.shortcuts import render, redirect
from .forms import LockForm
from .models import Lock, Customer

from django.shortcuts import render, redirect, get_object_or_404


def lock_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        form = LockForm(request.POST, instance=customer.lock_set.first())
        
        if form.is_valid():
            lock_instance = form.save(commit=False)
            lock_instance.customer = customer
            lock_instance.save()
            return redirect('process_selection', customer_id=customer.id)
        else:
            print(form.errors)

    else:
        form = LockForm(instance=customer.lock_set.first())

    context = {
        'form': form,
        'customer': customer,
        'round_subtypes': json.dumps(LockForm.ROUND_SUBTYPES),
        'latch_subtypes': json.dumps(LockForm.LATCH_SUBTYPES),
        'motislock_subtypes': json.dumps(LockForm.MOTISLOCK_SUBTYPES)
    }

    return render(request, 'lock_selection.html', context)



def finish_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Use related_name to get the Finish instance for the customer, if exists
    finish_instance = Finish.objects.filter(customer=customer).first()
    
    if request.method == "POST":
        form = FinishForm(request.POST, instance=finish_instance)

        if form.is_valid():
            new_finish = form.save(commit=False)
            new_finish.customer = customer
            new_finish.save()
            return redirect('process_selection', customer_id=customer.id)
        
    else:
        form = FinishForm(instance=finish_instance)

    context = {
        'form': form,
        'customer': customer,
        'finish_exists': bool(finish_instance)  # Returns True if finish_instance exists, otherwise False
    }

    return render(request, 'finish_selection.html', context)


def door_open_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if the customer already has a DoorOpen selection
    door_open_instance = DoorOpen.objects.filter(customer=customer).first()

    if request.method == "POST":
        form = DoorOpenForm(request.POST, instance=door_open_instance)

        if form.is_valid():
            door_open = form.save(commit=False)
            door_open.customer = customer
            door_open.save()
            return redirect('process_selection', customer_id=customer.id)
    else:
        form = DoorOpenForm(instance=door_open_instance)

    context = {
        'form': form,
        'customer': customer,
        'door_open_exists': bool(door_open_instance)
    }

    return render(request, 'door_open_selection.html', context)


from .models import Frame, Customer, Measurement
from .forms import FrameForm
from django.shortcuts import render, get_object_or_404, redirect

FRAME_ADJUSTMENTS = {
    'Small': (-7.3, -7.3, -4.3),
    'Normal': (-7.3, -7.3, -4.8),
    'Medium': (-7.3, -7.3, -4.3),
    'Heavy': (-11, -11, -6.3),
    'DoorWithoutClearence': (0, 0, 0),
    'DoorWithClearence': (-0.7, -0.7, -0.8)
}

def frame_selection(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    
    # Check if Measurement exists for the customer
    try:
        initial_measurements = Measurement.objects.get(customer=customer)
    except Measurement.DoesNotExist:
        messages.error(request, "Measurement data is missing for the customer.")
        return redirect('process_selection', customer_id=customer.id)  # Assuming you have a URL pattern named 'process_selection'

    frame_exists = Frame.objects.filter(customer=customer).exists()
    if frame_exists:
        instance = Frame.objects.get(customer=customer)
    else:
        instance = None

    if request.method == 'POST':
        form = FrameForm(request.POST, instance=instance)
        if form.is_valid():
            frame = form.save(commit=False)
            adjustment = FRAME_ADJUSTMENTS.get(frame.type)
            if adjustment:
                frame.top_measurement = initial_measurements.top + adjustment[0]
                frame.breadth_measurement = initial_measurements.bottom + adjustment[1]
                frame.height_measurement = initial_measurements.height + adjustment[2]
            frame.customer = customer
            frame.save()
            return redirect('process_selection', customer_id=customer.id)  # Redirect back to the process selection

    else:
        form = FrameForm(instance=instance)

    context = {
        'form': form,
        'customer': customer,
        'frame_exists': frame_exists
    }
    return render(request, 'frame_selection.html', context)



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