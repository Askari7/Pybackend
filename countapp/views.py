import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Record  # Import the Record model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils import timezone
from .models import Record
from django.utils import timezone
from django.http import JsonResponse
from .models import Record  # Import your Record model
from datetime import datetime
from django.utils import timezone
import pytz
from .models import Record  # Import your Record model
@csrf_exempt  # Disable CSRF for this view
def get_data(request):
    if request.method == 'GET':
        try:
            # Retrieve startDate, startTime, and endTime from query parameters
            start_date_str = request.GET.get('startDate', None)
            start_time_str = request.GET.get('startTime', None)
            end_time_str = request.GET.get('endTime', None)
            print("here 1")
            print(start_date_str,start_time_str,end_time_str)
            # Initialize filter criteria
            filter_criteria = {}
            records = []  # Assume this is your queryset that contains the data

            # Parse the startDate if provided
            if start_date_str:
                try:

                    start_date = datetime.strptime(start_date_str, "%b %d, %Y, %I:%M %p")
                    print("here 2")
                    print(start_date)

                    filter_criteria['timestamp__date'] = start_date.date()  # Filter for records with the exact start_date
                    print(filter_criteria)
                    print("here 3")

                except ValueError as ve:
                    print(f"ValueError: {ve}")  # Log the error for debugging
                    return JsonResponse({'error': 'Invalid start date format'}, status=400)

            # Parse start time
            start_time = None
            if start_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, "%H:%M").time()  # Expected format: HH:MM
                    print(start_time)
                    print("here 4")

                except ValueError as ve:
                    print(f"ValueError: {ve}")  # Log the error for debugging
                    return JsonResponse({'error': 'Invalid start time format'}, status=400)

            # Parse end time
            end_time = None
            if end_time_str:
                try:
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()  # Expected format: HH:MM
                    print(end_time)
                    print("here 5")

                except ValueError as ve:
                    print(f"ValueError: {ve}")  # Log the error for debugging
                    return JsonResponse({'error': 'Invalid end time format'}, status=400)

            # Query the records based on the date filter
            if filter_criteria:
                print("filter_criteria",filter_criteria)
                print("here 6")

                records = Record.objects.filter(**filter_criteria)
            else:
                records = Record.objects.all()  # Get all records if no filter is applied

            if start_time or end_time:
                print("start_time", "end_time", start_time, end_time)
                print("here 7")

                # Convert start and end times to 24-hour format for filtering
                start_time_24_hour = convert_to_24_hour_format(datetime.combine(datetime.today(), start_time)) if start_time else None
                end_time_24_hour = convert_to_24_hour_format(datetime.combine(datetime.today(), end_time)) if end_time else None
                print("here 8")

                if start_time and end_time:
                    records = records.filter(timestamp__time__range=(start_time_24_hour, end_time_24_hour))  # Use time objects for range filtering
                elif start_time:  # If only startTime is provided
                    records = records.filter(timestamp__time__gte=start_time_24_hour)
                elif end_time:  # If only endTime is provided
                    records = records.filter(timestamp__time__lte=end_time_24_hour)

# Prepare the records data for the response

            # Prepare the records data for the response
            records_data = [
                {
                    'in_count': record.in_count,
                    'out_count': record.out_count,
                    'timestamp': record.timestamp.isoformat()  # Convert timestamp to ISO format for JSON
                }
                for record in records
            ]

            # Respond with the records data
            return JsonResponse({'records': records_data}, status=200)
        except Exception as e:
            print(f"Unexpected error: {e}")  # Log unexpected errors
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def convert_to_24_hour_format(time_obj):
    """Convert a time object to 24-hour format string."""
    return time_obj.strftime("%H:%M")  # 24-hour format (HH:MM)



# def save_record(request):
#     if request.method == 'POST':
#         try:
#             # Load JSON data from request body
#             data = json.loads(request.body)
#             # Extract values from the JSON data
#             total_in = data.get("Total in")
#             print(total_in,'total_in')
#             in_count = data.get("In")
#             out_count = data.get("Out")
#             time_value = data.get("Time")

#             # Convert time_value to timezone-aware datetime
#             if time_value:
#                 timestamp = timezone.datetime.strptime(time_value, '%Y-%m-%d %H:%M:%S')
#                 timestamp = timezone.make_aware(timestamp)  # Make it timezone-aware
#             else:
#                 timestamp = timezone.now()  # Use the current time if not provided

#             # Create a new Record instance and save it to the database
#             record = Record(in_count=in_count, out_count=out_count, timestamp=timestamp)
#             record.save()

#             # Respond with a success message
#             response = {
#                 'message': 'Data received and saved successfully',
#                 'data': {
#                     'In': in_count,
#                     'Out': out_count,
#                     'Time': time_value,
#                     "Total In":total_in,
#                 }
#             }
#             return JsonResponse(response, status=201)

#         except KeyError as e:
#             return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid data type or value.'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)




class MyPostView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract values from the incoming JSON data
            data = request.data  # `request.data` contains the JSON payload
            total_count = data.get("Total in")
            in_count = data.get("In")
            out_count = data.get("Out")
            time_value = data.get("Time")
            print(total_count,'total_in')

            # Convert time_value to timezone-aware datetime
            if time_value:
                timestamp = timezone.datetime.strptime(time_value, '%Y-%m-%d %H:%M:%S')
                timestamp = timezone.make_aware(timestamp)  # Make it timezone-aware
            else:
                timestamp = timezone.now()  # Use the current time if not provided
            print(total_count)
            # Create a new Record instance and save it to the database
            record = Record(in_count=in_count, out_count=out_count, timestamp=timestamp,total_count=total_count)
            print(record)
            record.save()  # Save the record to the database

            # Respond with a success message
            response = {
                'message': 'Data received and saved successfully',
                'data': {
                    'In': in_count,
                    'Out': out_count,
                    'Time': time_value,
                    "Total In":total_count,

                }
            }
            print(response)
            return Response(response, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid data type or value.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)