from django.db import models
from datetime import date, timedelta
import json


class Customer(models.Model):
    STATUS_CHOICES = [("COMPLETE", "COMPLETE"), ("PENDING", "PENDING")]
    PRIORITY_CHOICES = [("HIGH", "HIGH"), ("LESS", "LESS")]

    agent = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15
    )  # You can adjust the max length as required.
    google_location = models.URLField(
        blank=True
    )  # Assuming this will store a URL to the Google Maps location
    delivery_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    form_complete = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="PENDING")
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default="high")

    def __str__(self):
        return self.name


class Door(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="doors"
    )

    # Each process for a door
    measurement = models.OneToOneField(
        "Measurement", on_delete=models.SET_NULL, blank=True, null=True
    )
    hinge_selection = models.OneToOneField(
        "Hinge", on_delete=models.SET_NULL, blank=True, null=True
    )
    lock_selection = models.OneToOneField(
        "Lock", on_delete=models.SET_NULL, blank=True, null=True
    )
    finish_selection = models.OneToOneField(
        "Finish", on_delete=models.SET_NULL, blank=True, null=True
    )
    door_open_selection = models.OneToOneField(
        "DoorOpen", on_delete=models.SET_NULL, blank=True, null=True
    )
    frame_selection = models.OneToOneField(
        "Frame", on_delete=models.SET_NULL, blank=True, null=True
    )
    remark_selection= models.OneToOneField(
        "Remarks", on_delete=models.SET_NULL, blank=True, null=True,related_name="doors"
    )
    model_selection = models.OneToOneField(
        "DoorModel",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="model_selection",
    )
    glass_type_selection = models.OneToOneField(
        "GlassType",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="glass_type_selection",
    )
    primary_colour_selection = models.OneToOneField(
        "PrimaryColour",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="primary_colour_selection",
    )
    secondary_colour_selection = models.OneToOneField(
        "SecondaryColour",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="secondary_colour_selection",
    )
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Door {self.id} for {self.customer.name}"

    def completed_processes_count(self):
        processes = [
            self.measurement,
            self.hinge_selection,
            self.lock_selection,
            self.finish_selection,
            self.door_open_selection,
            self.frame_selection,
        ]
        return int(sum(1 for p in processes if p))

    @classmethod
    def total_processes_count(cls):
        # Count all OneToOne fields which represent the processes
        return sum(
            1
            for field in cls._meta.get_fields()
            if isinstance(field, models.OneToOneField)
        )

    def is_all_processes_completed(self):
        # First, we check if all the required processes are completed
        required_processes = [
            self.measurement,
            self.hinge_selection,
            self.lock_selection,
            self.finish_selection,
            self.door_open_selection,
            self.frame_selection,
            self.model_selection,
            self.primary_colour_selection,
        ]

        if not all(required_processes):
            return False

        # Since secondary_colour_selection and glass_type_selection are optional,
        # their presence or absence doesn't affect the completion status
        return True


class Measurement(models.Model):
    top = models.FloatField()
    bottom = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return f"T:{self.top}, B:{self.bottom}, H:{self.height}"


class Hinge(models.Model):
    HINGE_CHOICES = [("RH", "RH"), ("LH", "LH")]
    type = models.CharField(choices=HINGE_CHOICES, max_length=2)

    def __str__(self):
        return (
            self.get_type_display()
        )  # Django method to get the human-readable choice.


class Lock(models.Model):
    LOCK_CHOICES = [
        ("Round", "Round"),
        ("Latch", "Latch"),
        ("Motislock", "Motislock"),
        ("ALLdroplock", "ALLdroplock"),
    ]
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
    OPEN_CHOICES = [("out", "Out"), ("in", "In")]
    direction = models.CharField(choices=OPEN_CHOICES, max_length=3)

    def __str__(self):
        return self.get_direction_display()


class Frame(models.Model):
    FRAME_CHOICES = [
        ("Small", "Small"),
        ("Normal", "Normal"),
        ("Medium", "Medium"),
        ("Heavy", "Heavy"),
        ("Door Without Clearence", "Door Without Clearence"),
        ("Door With Clearence", "Door With Clearence"),
    ]
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

class Remarks(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=10000)

    def __str__(self):
        return self.remarks


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


class DoorBatch(models.Model):
    date = models.DateField(unique=True)
    doors = models.ManyToManyField("Door")
    is_complete = models.BooleanField(default=False)

    def mark_as_complete(self):
        """
        Marks the batch as complete and sets all its doors' finish status to True.
        """
        if not self.is_complete:
            self.is_complete = True
            self.save()
            for door in self.doors.all():
                door.finished = True
                door.save()

    def remove_door(self, door):
        """
        Removes a door from the batch and doesn't mark its finish status.
        """
        door.finished = False
        door.save()
        self.doors.remove(door)
    
    @classmethod
    def create_batch_for_today(cls):
        todays_batch, created = cls.objects.get_or_create(date=date.today())
        if created:  # if a new batch was created for today
            filename = 'mould_data.json'
                # Load the data from the JSON file
            with open(filename, 'r') as file:
                mold_data = json.load(file)
            # Use the logic from your 'show_pdf_for_day' view to populate the batch:
            all_doors = (
                Door.objects.filter(finished=False)
                .filter(customer__form_complete=True)
                .order_by("customer__delivery_date")
            )
            for door in all_doors:
                model_name = door.model_selection.model_name.lower()
                if model_name in mold_data and mold_data[model_name] > 0:
                    todays_batch.doors.add(door)
                    mold_data[model_name] -= 1
        return todays_batch

    def __str__(self):
        return f"Batch for {self.date}"
