from django.db import models

class Customer(models.Model):
    STATUS_CHOICES = [('COMPLETE', 'COMPLETE'), ('PENDING', 'PENDING')]

    agent = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # You can adjust the max length as required.
    google_location = models.URLField(blank=True)  # Assuming this will store a URL to the Google Maps location
    delivery_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    form_complete = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="PENDING")
    
    def __str__(self):
        return self.name


class Door(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="doors")

    # Each process for a door
    measurement = models.OneToOneField('Measurement', on_delete=models.SET_NULL, blank=True, null=True)
    hinge_selection = models.OneToOneField('Hinge', on_delete=models.SET_NULL, blank=True, null=True)
    lock_selection = models.OneToOneField('Lock', on_delete=models.SET_NULL, blank=True, null=True)
    finish_selection = models.OneToOneField('Finish', on_delete=models.SET_NULL, blank=True, null=True)
    door_open_selection = models.OneToOneField('DoorOpen', on_delete=models.SET_NULL, blank=True, null=True)
    frame_selection = models.OneToOneField('Frame', on_delete=models.SET_NULL, blank=True, null=True)
    model_selection = models.OneToOneField('DoorModel', on_delete=models.SET_NULL, blank=True, null=True, related_name='model_selection')
    glass_type_selection = models.OneToOneField('GlassType', on_delete=models.SET_NULL, blank=True, null=True, related_name='glass_type_selection')
    primary_colour_selection = models.OneToOneField('PrimaryColour', on_delete=models.SET_NULL, blank=True, null=True, related_name='primary_colour_selection')
    secondary_colour_selection = models.OneToOneField('SecondaryColour', on_delete=models.SET_NULL, blank=True, null=True, related_name='secondary_colour_selection')
    def __str__(self):
        return f"Door {self.id} for {self.customer.name}"
    def completed_processes_count(self):
        processes = [
            self.measurement,
            self.hinge_selection,
            self.lock_selection,
            self.finish_selection,
            self.door_open_selection,
            self.frame_selection
        ]
        return int(sum(1 for p in processes if p))
    @classmethod
    def total_processes_count(cls):
        # Count all OneToOne fields which represent the processes
        return sum(1 for field in cls._meta.get_fields() if isinstance(field, models.OneToOneField))
    
    def is_all_processes_completed(self):
        return self.completed_processes_count() == Door.total_processes_count()




class Measurement(models.Model):
    top = models.FloatField()
    bottom = models.FloatField()
    height = models.FloatField()
    def __str__(self):
        return f"Top:{self.top}, Bottom:{self.bottom}, Height:{self.height}"
    

class Hinge(models.Model):
    HINGE_CHOICES = [('RH', 'RH'), ('LH', 'LH')]
    type = models.CharField(choices=HINGE_CHOICES, max_length=2)
    def __str__(self):
        return self.get_type_display()  # Django method to get the human-readable choice.

class Lock(models.Model):
    LOCK_CHOICES = [('Round', 'Round'), ('Latch', 'Latch'), 
                   ('Motislock', 'Motislock'), ('ALLdroplock', 'ALLdroplock')]
    type = models.CharField(choices=LOCK_CHOICES, max_length=20)
    sub_type = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.get_type_display()} - {self.sub_type}"

class Finish(models.Model):
    front = models.CharField(max_length=20)
    back = models.CharField(max_length=20)
    def __str__(self):
        return f"Front: {self.front}, Back: {self.back}"

class DoorOpen(models.Model):
    OPEN_CHOICES = [('out', 'Out'), ('in', 'In')]
    direction = models.CharField(choices=OPEN_CHOICES, max_length=3)
    def __str__(self):
        return self.get_direction_display()

class Frame(models.Model):
    FRAME_CHOICES = [('Small', 'Small'), ('Normal', 'Normal'), 
                     ('Medium', 'Medium'), ('Heavy', 'Heavy'),
                     ('Door Without Clearence', 'Door Without Clearence'), 
                     ('Door With Clearence', 'Door With Clearence')]
    type = models.CharField(choices=FRAME_CHOICES, max_length=50)
    top_measurement = models.FloatField()
    breadth_measurement = models.FloatField()
    height_measurement = models.FloatField()
    def __str__(self):
        return f"{self.get_type_display()} \n - T:{self.top_measurement}, B:{self.breadth_measurement}, H:{self.height_measurement}"

class DoorModel(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    def __str__(self):
        return self.model_name

class ColorCombination(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)
    def __str__(self):
        return self.color_name

class PrimaryColour(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)
    def __str__(self):
        return self.color_name
    
class SecondaryColour(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)
    def __str__(self):
        return self.color_name


class GlassType(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    glass_name = models.CharField(max_length=100)
    def __str__(self):
        return self.glass_name

