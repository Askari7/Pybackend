import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from channels.db import database_sync_to_async  # Import this for async database operations

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accept the connection

    async def disconnect(self, close_code):
        pass  # Handle disconnection if needed (e.g., cleanup)

    async def receive(self, text_data):
        from .models import Record  # Move the import here to avoid loading issues

        try:
            data = json.loads(text_data)  # Load the incoming data
            
            # Extract values from the JSON data
            in_count = data.get("In")
            out_count = data.get("Out")
            time_value = data.get("Time")

            # Convert time_value to timezone-aware datetime
            if time_value:
                timestamp = timezone.datetime.strptime(time_value, '%Y-%m-%d %H:%M:%S')
                timestamp = timezone.make_aware(timestamp)  # Make it timezone-aware
            else:
                timestamp = timezone.now()  # Use the current time if not provided

            # Create a new Record instance and save it to the database
            record = Record(in_count=in_count, out_count=out_count, timestamp=timestamp)
            await database_sync_to_async(record.save)()  # Save record asynchronously

            # Respond with a success message
            response = {
                'message': 'Data received and saved successfully',
                'data': {
                    'In': in_count,
                    'Out': out_count,
                    'Time': time_value
                }
            }
            await self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format.'
            }))
        except KeyError as e:
            await self.send(text_data=json.dumps({
                'error': f'Missing key: {str(e)}'
            }))
        except ValueError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid data type or value.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': 'An unexpected error occurred: ' + str(e)
            }))
