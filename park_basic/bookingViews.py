
from rest_framework.decorators import api_view


from park_basic.models import booking
@api_view(['GET'])
def insert_data():
    # Create an instance of the model
    new_data = booking(
        #set the feild data,
        Date=timezone.now,
        Time ='',
        reserverId ='001',
        slotId ='PS01'
    )
    # Save the instance to the database
    new_data.save()
