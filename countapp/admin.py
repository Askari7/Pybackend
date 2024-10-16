# admin.py
from django.contrib import admin
from .models import Record  # Import the Record model

# Register the Record model with the admin site
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('in_count', 'out_count', 'timestamp')  # Customize the list display
    search_fields = ('in_count', 'out_count')  # Add search functionality
    list_filter = ('timestamp',)  # Add filtering by timestamp

    # Optionally, you can customize other admin options here

