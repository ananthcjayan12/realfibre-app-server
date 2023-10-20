from django import forms
from .models import Customer, Door, Measurement, Hinge, Lock, Finish, DoorOpen, Frame

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'location']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['top', 'bottom', 'height']

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
        fields = ['type', 'top_measurement', 'breadth_measurement', 'height_measurement']

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

