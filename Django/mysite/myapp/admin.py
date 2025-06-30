from django.contrib import admin
from .models import Product  # Import the model you created

admin.site.register(Product)  # Register it so it appears in admin