from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CustomerForm, MeasurementForm, HingeForm, LockForm, FinishForm, DoorOpenForm, FrameForm, AdvancePaymentForm,DoorForm ,AgentCreationForm,CustomerFilterForm,UpdatePriorityForm
from django.http import HttpResponseForbidden
from django.contrib import messages
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.templatetags.static import static

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
        print(request.user)
        customers = Customer.objects.filter(agent=request.user, name__icontains=query)[:5]  # Added search functionality and limited to first 5

    return render(request, 'home.html', {'customers': customers, 'form': form})



def door_selection(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    doors = Door.objects.filter(customer=customer).order_by('id')
    no_of_doors=len(doors)
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
        'show_submit_order_button': all_doors_completed and not customer.form_complete and no_of_doors != 0  and customer.delivery_date,
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
    return render_pdf('admin_pdf_template.html', {'doors': doors, 'customer': customer})


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
    form = CustomerFilterForm(request.GET)
    customers = Customer.objects.filter(form_complete=True)

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        form = UpdatePriorityForm(request.POST, instance=Customer.objects.get(id=customer_id))
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')

    if form.is_valid():
        data = form.cleaned_data
        delivery_date_from = data.get('delivery_date_from')
        delivery_date_to = data.get('delivery_date_to')
        customer_search = data.get('customer_search')
        status = data.get('status')
        priority = data.get('priority')

        if delivery_date_from and delivery_date_to:
            customers = customers.filter(delivery_date__range=[delivery_date_from, delivery_date_to])
        if customer_search:
            customers = customers.filter(name__icontains=customer_search)
        if status:
            if status == 'due':
                customers = customers.filter(status="PENDING", delivery_date__lte=datetime.now().date())
            elif status == 'upcoming':
                upcoming_date = datetime.now().date() + timedelta(days=7)
                customers = customers.filter(status="PENDING", delivery_date__range=[datetime.now().date(), upcoming_date])
            elif status == 'pending':
                customers = customers.filter(status="PENDING")
            elif status == 'completed':
                customers = customers.filter(status="COMPLETE")
        if priority:
            customers = customers.filter(priority=priority)

    context = {
        'customers': customers,
        'form': form,
    }
    return render(request, 'admin_dashboard.html', context)


def mark_as_complete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.status = 'COMPLETE'
    customer.save()
    return redirect('admin_dashboard')
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


from django.templatetags.static import static


def door_and_glass_selector_view(request,door_id):
    door_instance = get_object_or_404(Door, id=door_id)

    if request.method == 'POST':
        door_model_name = request.POST.get('doormodel')
        primary_color_name = request.POST.get('primarycolour')
        secondary_color_name = request.POST.get('secondarycolour')
        glass_type_name = request.POST.get('glasstype')

        if door_model_name:
            door_model_instance, created = DoorModel.objects.get_or_create(model_name=door_model_name, door=door_instance)
            door_instance.model_selection = door_model_instance
        else :
            door_instance.model_selection = None

        if primary_color_name:
            primary_color_instance, created = PrimaryColour.objects.get_or_create(color_name=primary_color_name, door=door_instance)
            door_instance.primary_colour_selection = primary_color_instance
        else :
            door_instance.primary_colour_selection = None


        if secondary_color_name:
            secondary_color_instance, created = SecondaryColour.objects.get_or_create(color_name=secondary_color_name, door=door_instance)
            door_instance.secondary_colour_selection = secondary_color_instance
        else :
            door_instance.secondary_colour_selection = None

        if glass_type_name:
            glass_type_instance, created = GlassType.objects.get_or_create(glass_name=glass_type_name, door=door_instance)
            door_instance.glass_type_selection = glass_type_instance
        else :
            door_instance.glass_type_selection = None

        door_instance.save()
        return redirect('process_selection', door_id=door_instance.id)  # Redirect back to the process selection


    # List of door names (extracted from your image filenames)
    doors = [
        "petra", "triangle", "astonia", "cloud", "delta", "flora", "hexa", "horizon", "liva", "mars", "milton",
        "narrow", "periyar", "rectaglass", "regal", "regency", "richmond", "rivera", "simplon", "skill",
        "spasio", "vector", "venues", "vetrix", "wayanad", "wexco", "wexcoglass","venuesglass"
    ]

    # Dictionary mapping doors to their associated glasses
    door_glass_mapping = {
    "delta": ["EL01", "EL02", "EL03", "EL04", "EL05", "EL06", "EL07", "EL08", "EL09", "EL10"],
    "cloud": [f"PY{i:02}" for i in range(1, 13)],  # PY01 to PY12
    "simplon": [f"PK{i:02}" for i in range(1, 11)],  # PK01 to PK10
    "hexa": [f"XA{i:02}" for i in range(1, 10)],  # XA01 to XA09
    "wexcoglass": [f"GL{i:02}" for i in range(1, 11)],  # GL01 to GL10
    "rectaglass": [f"GL{i:02}" for i in range(11, 21)],  # GL11 to GL20
    "vector": [f"TR{i:02}" for i in range(1, 11)],  # TR01 to TR10
    "horizon": [f"RZ{i:02}" for i in range(1, 13)],  # RZ01 to RZ12
    "astonia": [f"TB{i:02}" for i in range(1, 11)],  # TB01 to TB10
    "liva": [f"AV{i:02}" for i in range(1, 12)],  # AV01 to AV11
    "venuesglass": [f"V{i:02}" for i in range(1, 10)]  # V01 to V09
}


    # Create the static paths for door images and their respective glasses
    door_images_js = {door: static(f'doors/{door}.png') for door in doors}
    door_glass_mapping_js = {door: [static(f'glass/{glass}.png') for glass in glasses] for door, glasses in door_glass_mapping.items()}
    door_images_json = json.dumps(door_images_js)
    door_glass_mapping_json = json.dumps(door_glass_mapping_js) 
    colors = [
    "coffee", "darkgrey", "eeti", "leatherfinish", "lightgrey", "mahagani",
    "teakwooddark", "teakwoodlight", "white"
]
    color_images_js = {color: static(f'colours/{color}.png') for color in colors}
    colors_mapping_json = json.dumps(color_images_js)
    current_door_model = door_instance.model_selection.model_name if door_instance.model_selection else None
    current_primary_color = door_instance.primary_colour_selection.color_name if door_instance.primary_colour_selection else None
    current_secondary_color = door_instance.secondary_colour_selection.color_name if door_instance.secondary_colour_selection else None
    current_glass_type = door_instance.glass_type_selection.glass_name if door_instance.glass_type_selection else None



    context = {
        'doors': doors,
        'door_glass_mapping': door_glass_mapping,
        'door_images_json': door_images_json,
        'door_glass_mapping_json': door_glass_mapping_json,
        'colors_mapping_json': colors_mapping_json,
       'colors' :colors,
       'door_instance':door_instance,
       'current_door_model': current_door_model,
        'current_primary_color': current_primary_color,
        'current_secondary_color': current_secondary_color,
        'current_glass_type': current_glass_type,
               } 
    

    return render(request, 'doorglass1.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def update_balance(request):
    data = json.loads(request.body)
    customer_id = data.get('customer_id')
    new_balance = data.get('new_balance')
    
    # Update the customer's balance amount in the database
    # Make sure to handle any potential errors and respond accordingly
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.balance_amount = new_balance
        customer.save()
        return JsonResponse({'success': True})
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Customer not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def update_priority(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        customer_id = data.get('customer_id')
        new_priority = data.get('new_priority')
        
        customer = Customer.objects.get(id=customer_id)
        customer.priority = new_priority
        customer.save()
        return JsonResponse({'success': True})
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

from django.db.models import Q

def show_pdf_for_day(request):
    mold_data = {
    'astoni': 1,
    'cloud': 4,
    'delta': 4,
    'flora': 1,
    'horizon': 2,
    'hexa': 6,
    'liva': 2,
    'milton': 2,
    'mars': 1,
    'petra': 3,
    'periyar': 2,
    'regal': 1,
    'rectaglass': 2,  # Assuming 'recta' corresponds to 'rectaglass' in the mold list
    'regency': 4,
    'rivera': 5,
    'spasio': 5,
    'skill': 3,
    'simplon': 2,
    'vector': 2,
    'venues': 2,
    'wexco': 2,
    'richmond': 3,  # Assuming 'richmound' corresponds to 'richmond' in the mold list
    'wayanad': 3,
    'vetrix': 1,
    'triangle': 0,
    'narrow': 0,
    'wexcoglass': 0
}


    today = date.today()
    try:
        existing_batch = DoorBatch.objects.get(date=today)
    except DoorBatch.DoesNotExist:
        existing_batch = None

    # If a batch exists for today, fetch doors from it
    if existing_batch:
        fulfilled_doors = list(existing_batch.doors.all())
    else:
        # If no batch for today, prepare a new batch
        all_doors = Door.objects.filter(finished=False).filter(customer__form_complete=True).order_by('customer__delivery_date')
        fulfilled_doors = []

        for door in all_doors:
            try:
                model_name = door.model_selection.model_name.lower()
                if model_name in mold_data and mold_data[model_name] > 0:
                    fulfilled_doors.append(door)
                    mold_data[model_name] -= 1
            except:
                pass

        # Create a new batch for today and add the prepared doors to it
        new_batch = DoorBatch(date=today)
        new_batch.save()
        new_batch.doors.add(*fulfilled_doors)

    customers = [door.customer for door in fulfilled_doors]
    return render_pdf('customer_to_be_print.html', {'doors': fulfilled_doors, 'customers': customers})


def door_batch_dashboard(request):
    # Get today's batch or None
    todays_batch = DoorBatch.objects.filter(date=date.today()).first()

    # If batch is not available, create a new batch
    if not todays_batch:
        todays_batch = DoorBatch.create_batch_for_today()

    if request.method == 'POST':
        if 'complete_batch' in request.POST:
            todays_batch.mark_as_complete()
            return redirect('door_batch_dashboard')
        elif 'remove_door' in request.POST:
            door_id = request.POST.get('door_id')
            door = Door.objects.get(pk=door_id)
            todays_batch.remove_door(door)
            return redirect('door_batch_dashboard')
        elif 'reset_batch' in request.POST:
            todays_batch.delete()
            return redirect('door_batch_dashboard') 

    return render(request, 'door_batch_dashboard.html', {'batch': todays_batch})



def doorwise_dashboard(request):
    context = {}
    all_doors = Door.objects.filter(customer__form_complete=True)

    # If no filters, show all doors
    context['filter'] = "All Doors"
    
    # Check for 'finished' filter
    if request.GET.get('finished') is not None:
        status = request.GET.get('finished').lower() == 'true'
        all_doors = all_doors.filter(finished=status)
        context['filter'] += f", Finished: {status}"

    # Check for 'glass_selected' filter
    if request.GET.get('glass_selected'):
        all_doors = all_doors.filter(glass_type_selection__isnull=False)
        context['filter'] += ", Doors with Glass Selection"

    # Check for 'delivery_date' filter
    if request.GET.get('delivery_date'):
        date_filter = request.GET.get('delivery_date')
        all_doors = all_doors.filter(customer__delivery_date=date_filter)
        context['filter'] += f", Delivery Date: {date_filter}"


    context['doors'] = all_doors

    return render(request, 'door_dashboard.html', context)

