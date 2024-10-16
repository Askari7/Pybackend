from django.urls import path
from .views import get_data , MyPostView # Import the view

urlpatterns = [
    path('get-data/', get_data, name='get_data'),  # Ensure this matches your desired endpoint
    path('api/save-record/', MyPostView.as_view(), name='save-record'),

]