from django.db import models

class Customer(models.Model):
    agent = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def is_measurement_completed(self):
        return Measurement.objects.filter(customer=self).exists()

    def is_hinge_selection_completed(self):
        return Hinge.objects.filter(customer=self).exists()

    def is_lock_selection_completed(self):
        return Lock.objects.filter(customer=self).exists()

    def is_finish_selection_completed(self):
        return Finish.objects.filter(customer=self).exists()

    def is_door_open_selection_completed(self):
        return DoorOpen.objects.filter(customer=self).exists()

    def is_frame_selection_completed(self):
        return Frame.objects.filter(customer=self).exists()

    def is_advance_payment_updated(self):
        return self.advance_paid is not None and self.advance_paid > 0


class Measurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    top = models.FloatField()
    bottom = models.FloatField()
    height = models.FloatField()

class Hinge(models.Model):
    HINGE_CHOICES = [('RH', 'RH'), ('LH', 'LH')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(choices=HINGE_CHOICES, max_length=2)

# Definitions for door model, color combination, and glass type
class DoorModel(models.Model):
    model_name = models.CharField(max_length=100)

class ColorCombination(models.Model):
    color_name = models.CharField(max_length=100)

class GlassType(models.Model):
    glass_name = models.CharField(max_length=100)

# The actual door selection made by the user
class Door(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    door_model = models.ForeignKey(DoorModel, on_delete=models.CASCADE)
    color_combination = models.ForeignKey(ColorCombination, on_delete=models.CASCADE)
    glass_type = models.ForeignKey(GlassType, on_delete=models.CASCADE)

class Lock(models.Model):
    LOCK_CHOICES = [('Round', 'Round'), ('Latch', 'Latch'), 
                   ('Motislock', 'Motislock'), ('ALLdroplock', 'ALLdroplock')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(choices=LOCK_CHOICES, max_length=20)
    sub_type = models.CharField(max_length=20)

class Finish(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    front = models.CharField(max_length=20)
    back = models.CharField(max_length=20)

class DoorOpen(models.Model):
    OPEN_CHOICES = [('out', 'Out'), ('in', 'In')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    direction = models.CharField(choices=OPEN_CHOICES, max_length=3)

class Frame(models.Model):
    FRAME_CHOICES = [('Small', 'Small'), ('Normal', 'Normal'), 
                     ('Medium', 'Medium'), ('Heavy', 'Heavy'),
                     ('DoorWithoutClearence', 'DoorWithoutClearence'), 
                     ('DoorWithClearence', 'DoorWithClearence')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(choices=FRAME_CHOICES, max_length=20)
    top_measurement = models.FloatField()
    breadth_measurement = models.FloatField()
    height_measurement = models.FloatField()


