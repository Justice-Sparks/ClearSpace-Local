from django.db import models
from django.utils import timezone

#-------------------------------------------------------------------------------------------------------#
# MODELS: 
# We are telling Django: "This class represents a data base table, and each instance represents a row"

# All model classes inherit from django's base class called 'model' 
# 'models.Model' is used to locate it within the 'models' library we imported above. 
# By inheriting from it, Django knows this class should map to DB table,
# it automatically adds id(primary key), querymethods, and save/delete behavior 

#? WE DONT HAVE INIT METHODS (initializers)... why? 
#* Becuase Django already provides one in the base class 'Model' from the 'models' library. 
#* So these classes inherit a prebuild model-initializer-method 
#-------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------------------------------------------------------#
class City(models.Model):
    name = models.CharField(max_length=100) # Readable city name
    state = models.CharField(max_length=2)  # Two letters to rep state (make city name unique)
    slug = models.SlugField(unique=True)    # URL safe identifier 

    created_at = models.DateTimeField(auto_now_add=True)

    # Model Configuration: Instructions for how django should treat this table  
    class Meta:
        unique_together = ("name", "state") # Only unique combos of name+state can exist: No Dupes
        ordering = ["state", "name"]        # Defualt query sort order: 'Order by State, Name' (grouping cities by state)

    # Dunder method: Defines how object should appear when printed in string for (for UI)
    def __str__(self):
        return f"{self.name}, {self.state}"

#-------------------------------------------------------------------------------------------------------#
class ServiceCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

#-------------------------------------------------------------------------------------------------------#
class Client(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ("individual", "Individual"),
        ("company", "Company"),
    ]

    name = models.CharField(max_length=255)
    business_type = models.CharField(
        max_length=20,
        choices=BUSINESS_TYPE_CHOICES,
        default="company",
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="clients",
    )

    service_category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="clients",
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#-------------------------------------------------------------------------------------------------------#
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("assigned", "Assigned"),
        ("closed", "Closed"),
    ]

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )

    service_category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )

    assigned_client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)

    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_category} lead in {self.city}" 
