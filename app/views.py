from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CustomerForm, MeasurementForm, HingeForm, LockForm, FinishForm, DoorOpenForm, FrameForm, AdvancePaymentForm,DoorForm ,AgentCreationForm
from django.http import HttpResponseForbidden
from django.contrib import messages
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
FRAME_ADJUSTMENTS = {
    'Small': (-7.3, -7.3, -4.3),
    'Normal': (-7.3, -7.3, -4.8),
    'Medium': (-7.3, -7.3, -4.3),
    'Heavy': (-11, -11, -6.3),
    'Door Without Clearence': (0, 0, 0),
    'Door With Clearence': (-0.7, -0.7, -0.8)
}

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('home')
    
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
    all_doors_completed = all(door.is_all_processes_completed() for door in doors)
    if customer.delivery_date:
        formatted_date = customer.delivery_date.strftime('%Y-%m-%d')
    else:
        formatted_date = None

    if request.method == "POST":
        # Check for submit order button press
        if 'submit_order' in request.POST:
            customer.form_complete = True
            customer.order_date=datetime.now()
            customer.save()
            # Redirect or show a message here based on your design.
            return redirect('door_selection', customer_id=customer_id)
        # Logic to create a new door
        new_door = Door(customer=customer)
        new_door.save()
        # Redirect to the door selection page again to see the updated list
        return redirect('door_selection', customer_id=customer_id)
    
    context = {
        'customer': customer,
        'doors': doors,
        'show_submit_order_button': all_doors_completed and not customer.form_complete,
        'formatted_date':formatted_date
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
            lock = form.save(commit=False)
            door.lock_selection = lock
            lock.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = LockForm(instance=lock_instance)

    context = {
        'form': form,
        'door': door,
        'round_subtypes': json.dumps(LockForm.ROUND_SUBTYPES),
        'latch_subtypes': json.dumps(LockForm.LATCH_SUBTYPES),
        'motislock_subtypes': json.dumps(LockForm.MOTISLOCK_SUBTYPES)
    }
    
    return render(request, 'lock_selection.html', context)

@login_required
def finish_selection(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    finish_instance = door.finish_selection

    if request.method == "POST":
        form = FinishForm(request.POST, instance=finish_instance)
        if form.is_valid():
            finish = form.save(commit=False)
            door.finish_selection = finish
            finish.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = FinishForm(instance=finish_instance)

    context = {
        'form': form,
        'door': door
    }

    return render(request, 'finish_selection.html', context)




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
def door_open_selection(request, door_id):
    door = get_object_or_404(Door, id=door_id)
    door_open_instance = door.door_open_selection  # Adjust to your actual Door model's attribute name for DoorOpen

    if request.method == "POST":
        form = DoorOpenForm(request.POST, instance=door_open_instance)
        if form.is_valid():
            door_open = form.save(commit=False)
            door.door_open_selection = door_open
            door_open.save()
            door.save()
            return redirect('process_selection', door_id=door.id)
    else:
        form = DoorOpenForm(instance=door_open_instance)

    context = {
        'form': form,
        'door': door
    }

    return render(request, 'door_open_selection.html', context)



@login_required
def frame_selection(request, door_id):
    door = get_object_or_404(Door, pk=door_id)
    
    # Check if Measurement exists for the door
    if not door.measurement:
        messages.error(request, "Measurement data is missing for the door.")
        return redirect('process_selection', door_id=door.id)  # Assuming you have a URL pattern named 'process_selection'

    # Check if a Frame already exists for the door
    if door.frame_selection:
        instance = door.frame_selection
        frame_exists = True
    else:
        instance = Frame()
        frame_exists = False

    if request.method == 'POST':
        form = FrameForm(request.POST, instance=instance)
        if form.is_valid():
            frame = form.save(commit=False)
            adjustment = FRAME_ADJUSTMENTS.get(frame.type)
            if adjustment:
                frame.top_measurement = door.measurement.top + adjustment[0]
                frame.breadth_measurement = door.measurement.bottom + adjustment[1]
                frame.height_measurement = door.measurement.height + adjustment[2]
            
            frame.save()
            door.frame_selection = frame
            door.save()
            return redirect('process_selection', door_id=door.id)  # Redirect back to the process selection

    else:
        form = FrameForm(instance=instance)

    context = {
        'form': form,
        'door': door,
        'frame_exists': frame_exists
    }
    return render(request, 'frame_selection.html', context)

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'filename="customer_order.pdf"'  # Changed the filename
    pisa.CreatePDF(html, dest=result)
    return result

def show_pdf(request, customer_id):
    print(customer_id)
    customer = Customer.objects.get(pk=customer_id)
    doors = Door.objects.filter(customer=customer)
    return render_pdf('door_pdf_template.html', {'doors': doors, 'customer': customer})


def door_pdf_view(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    doors = Door.objects.filter(customer=customer)
    return render_pdf('door_pdf_template.html', {'doors': doors, 'customer': customer})


from datetime import datetime

def update_customer_details(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        delivery_date = request.POST.get('delivery_date')
        advance_paid = request.POST.get('advance_paid')
        
        # Convert the string representation of the date into a date object
        if delivery_date:
            try:
                formatted_delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
                customer.delivery_date = formatted_delivery_date
            except ValueError:
                import traceback
                # Handle date format error if necessary
                print(traceback.format_exc())
                pass

        if advance_paid:
            try:
                customer.advance_paid = float(advance_paid)
            except ValueError:
                # Handle conversion error if necessary
                pass
        
        customer.save()
        return redirect('door_selection', customer_id=customer_id)
    
from django.shortcuts import render
from .models import Customer, Door
from datetime import date, timedelta

from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Customer

from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Customer

def admin_dashboard(request):
    # By default, show all customers
    customers = Customer.objects.filter(form_complete=True)

    # Filter based on the delivery date range
    delivery_date_from = request.GET.get('delivery_date_from')
    delivery_date_to = request.GET.get('delivery_date_to')
    
    if delivery_date_from and delivery_date_to:
        customers = customers.filter(delivery_date__range=[delivery_date_from, delivery_date_to])
    
    # Search box for customer name
    customer_search = request.GET.get('customer_search')
    if customer_search:
        customers = customers.filter(name__icontains=customer_search)

    # Quick filter for Due Customers
    status = request.GET.get('status')
    if status == 'due':
        customers = customers.filter(status="PENDING").filter(form_complete=True).filter(delivery_date__lte=datetime.now().date())
    elif status == 'upcoming':
        upcoming_date = datetime.now().date() + timedelta(days=7)
        customers = customers.filter(status="PENDING").filter(form_complete=True).filter(delivery_date__range=[datetime.now().date(), upcoming_date])
    elif status == 'pending':
        upcoming_date = datetime.now().date() + timedelta(days=7)
        customers = customers.filter(status="PENDING").filter(form_complete=True)
    elif status == 'completed':
        upcoming_date = datetime.now().date() + timedelta(days=7)
        customers = customers.filter(status="COMPLETE").filter(form_complete=True)

    context = {
        'customers': customers,
    }

    return render(request, 'admin_dashboard.html', context)



def mark_as_complete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.status = 'COMPLETE'
    customer.save()
    return redirect('admin_dashboard')

def update_balance(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        # Update the customer's balance amount
        new_balance = request.POST.get('balance_amount')
        # Logic to update balance amount goes here
        return redirect('admin_dashboard')
    return render(request, 'update_balance_template.html', {'customer': customer})

from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect

def agent_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to agent's dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



def agent_logout(request):
    logout(request)
    return render(request, 'logout.html')

def create_agent(request):
    if not request.user.is_superuser:
        return redirect('home')  # redirecting if not superuser
    if request.method == "POST":
        form = AgentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # or wherever you'd like to redirect
    else:
        form = AgentCreationForm()
    return render(request, 'create_agent.html', {'form': form})