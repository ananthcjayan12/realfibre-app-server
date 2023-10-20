from django.db import models

class Customer(models.Model):
    agent = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    form_complete = models.BooleanField(default=False)

class Door(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="doors")

    # Each process for a door
    measurement = models.OneToOneField('Measurement', on_delete=models.SET_NULL, blank=True, null=True)
    hinge_selection = models.OneToOneField('Hinge', on_delete=models.SET_NULL, blank=True, null=True)
    lock_selection = models.OneToOneField('Lock', on_delete=models.SET_NULL, blank=True, null=True)
    finish_selection = models.OneToOneField('Finish', on_delete=models.SET_NULL, blank=True, null=True)
    door_open_selection = models.OneToOneField('DoorOpen', on_delete=models.SET_NULL, blank=True, null=True)
    frame_selection = models.OneToOneField('Frame', on_delete=models.SET_NULL, blank=True, null=True)

class Measurement(models.Model):
    top = models.FloatField()
    bottom = models.FloatField()
    height = models.FloatField()

class Hinge(models.Model):
    HINGE_CHOICES = [('RH', 'RH'), ('LH', 'LH')]
    type = models.CharField(choices=HINGE_CHOICES, max_length=2)

class Lock(models.Model):
    LOCK_CHOICES = [('Round', 'Round'), ('Latch', 'Latch'), 
                   ('Motislock', 'Motislock'), ('ALLdroplock', 'ALLdroplock')]
    type = models.CharField(choices=LOCK_CHOICES, max_length=20)
    sub_type = models.CharField(max_length=20)

class Finish(models.Model):
    front = models.CharField(max_length=20)
    back = models.CharField(max_length=20)

class DoorOpen(models.Model):
    OPEN_CHOICES = [('out', 'Out'), ('in', 'In')]
    direction = models.CharField(choices=OPEN_CHOICES, max_length=3)

class Frame(models.Model):
    FRAME_CHOICES = [('Small', 'Small'), ('Normal', 'Normal'), 
                     ('Medium', 'Medium'), ('Heavy', 'Heavy'),
                     ('DoorWithoutClearence', 'DoorWithoutClearence'), 
                     ('DoorWithClearence', 'DoorWithClearence')]
    type = models.CharField(choices=FRAME_CHOICES, max_length=20)
    top_measurement = models.FloatField()
    breadth_measurement = models.FloatField()
    height_measurement = models.FloatField()

class DoorModel(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)

class ColorCombination(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)

class GlassType(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    glass_name = models.CharField(max_length=100)

