from django import forms
from .models import Customer, Door, Measurement, Hinge, Lock, Finish, DoorOpen, Frame,Remarks
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'location', 'phone_number', 'google_location']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['top', 'bottom', 'height']

class RemarksForm(forms.ModelForm):
    class Meta:
        model = Remarks
        fields = ['remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # You can adjust rows and cols as needed
        }

class HingeForm(forms.ModelForm):
    class Meta:
        model = Hinge
        fields = ['type']

class LockForm(forms.ModelForm):
    
    ROUND_SUBTYPES = [('key', 'Key'), ('keyless', 'Keyless')]
    LATCH_SUBTYPES = [('normal', 'Normal'), ('spider_normal', 'Spider Normal'), ('spider_premium', 'Spider Premium')]
    MOTISLOCK_SUBTYPES = [('normal', 'Normal'), ('premium', 'Premium'), ('shortkey', 'Shortkey'), ('longkey', 'Longkey')]
    
    sub_type = forms.ChoiceField(choices=ROUND_SUBTYPES + LATCH_SUBTYPES + MOTISLOCK_SUBTYPES)

    class Meta:
        model = Lock
        fields = ['type', 'sub_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lock_type = self.data.get('type') if 'type' in self.data else self.initial.get('type')
        if lock_type == 'Round':
            self.fields['sub_type'].choices = self.ROUND_SUBTYPES
        elif lock_type == 'Latch':
            self.fields['sub_type'].choices = self.LATCH_SUBTYPES
        elif lock_type == 'Motislock':
            self.fields['sub_type'].choices = self.MOTISLOCK_SUBTYPES
        elif lock_type == 'ALLdroplock':
            self.fields['sub_type'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        lock_type = cleaned_data.get("type")
        sub_type = cleaned_data.get("sub_type")

        if lock_type == 'Round' and sub_type not in dict(self.ROUND_SUBTYPES):
            self.add_error('sub_type', 'Invalid choice for Round lock type.')
        elif lock_type == 'Latch' and sub_type not in dict(self.LATCH_SUBTYPES):
            self.add_error('sub_type', 'Invalid choice for Latch lock type.')
        elif lock_type == 'Motislock' and sub_type not in dict(self.MOTISLOCK_SUBTYPES):
            self.add_error('sub_type', 'Invalid choice for Motislock type.')

        return cleaned_data

class FinishForm(forms.ModelForm):
    FINISH_CHOICES = [('std', 'Std'), ('natural_wood', 'Natural Wood'), ('glossy', 'Glossy')]
    front = forms.ChoiceField(choices=FINISH_CHOICES)
    back = forms.ChoiceField(choices=FINISH_CHOICES)

    class Meta:
        model = Finish
        fields = ['front', 'back']

class DoorOpenForm(forms.ModelForm):
    class Meta:
        model = DoorOpen
        fields = ['direction']

class FrameForm(forms.ModelForm):
    class Meta:
        model = Frame
        fields = ['type']
        
class AdvancePaymentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['advance_paid']
        labels = {
            'advance_paid': 'Advance Paid'
        }

# New form to create a Door instance for a customer
class DoorForm(forms.ModelForm):
    class Meta:
        model = Door
        fields = []

class AgentCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords must match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomerFilterForm(forms.Form):
    delivery_date_from = forms.DateField(required=False)
    delivery_date_to = forms.DateField(required=False)
    customer_search = forms.CharField(max_length=100, required=False)
    status = forms.ChoiceField(choices=[('', 'All'), ('due', 'Due'), ('upcoming', 'Upcoming'), ('pending', 'Pending'), ('completed', 'Completed')], required=False)
    priority = forms.ChoiceField(choices=[('', 'All')] + Customer.PRIORITY_CHOICES, required=False)

class UpdatePriorityForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['priority']