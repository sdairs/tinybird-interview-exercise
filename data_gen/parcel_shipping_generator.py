import random
import datetime
from uuid import uuid4

columns = [
    'sender_id',
    'package_id',
    'recv_id',
    'courier_id',
    'status',
    'status_updated_at',
    'package_send_time',
    'package_deliv_time'
]

valid_status = [
    'awaiting_pickup',
    'picked_up',
    'transit_to_depot',
    'at_depot',
    'with_courier',
    'delivered',
    'missing',
    'returned_to_sender'
]

path_status = {
    1: [
        'awaiting_pickup',
        'picked_up',
        'transit_to_depot',
        'at_depot',
        'with_courier',
        'delivered'
    ],
    2: [
        'awaiting_pickup',
        'picked_up',
        'transit_to_depot',
        'missing',
    ],
    3: [
        'awaiting_pickup',
        'picked_up',
        'transit_to_depot',
        'at_depot',
        'with_courier',
        'at_depot',
        'returned_to_sender'
    ],
    4: [
        'awaiting_pickup',
        'picked_up',
        'transit_to_depot',
        'at_depot',
        'with_courier',
        'missing'
    ]
}

# Weighting for the frequency of status paths
# used by choices() https://docs.python.org/3/library/random.html#random.choices
path_status_weights = [80, 2, 15, 3]


def generate_dates(numdays):
    # Generate list of valid dates
    base = datetime.datetime(2020, 1, 1, hour=0, minute=0, second=0)
    return [base + datetime.timedelta(days=x) for x in range(numdays)]


valid_dates = generate_dates(30)


def generate_couriers():
    # Generate a list of UUIDs representing the current couriers
    return [str(uuid4()) for _ in range(1, 100)]


valid_couriers = generate_couriers()


def generate_regular_customers():
    # Generate a list of UUIDs representing recurring customers
    return [str(uuid4()) for _ in range(1, 100)]


regular_customers = generate_regular_customers()


def get_customer_id():
    # Get a UUID representing a customer
    # 25% chance of to pick a recurring customer ID
    # Remaining customer IDs will be random
    new_customer = random.randint(0, 20) % 5
    if new_customer:
        return str(uuid4())
    else:
        return random.choice(regular_customers)


def generate_random_timestamps_range(start, end, count):
    # Generates X number of timestamps between the start/end dates
    delta = (end-start).total_seconds()  # Seconds between start/end
    interval = delta / count
    times = [start]
    for i in range(0, count-1):
        times.append(times[i]+datetime.timedelta(seconds=interval))
    return times


def generate_parcel_path():
    # Generates an end-to-end 'path' of a parcel using the available paths defined in 'path_status'
    # A 'path' is the change in status of a parcel over time i.e. picked_up -> with_courier -> delivered
    # This simulated the journey that the parcel took
    path_results = []
    # Pick a random path from the dict of paths
    path = random.choices(list(path_status.keys()),
                          weights=path_status_weights, k=1)[0]
    steps = len(path_status[path])
    # How many days did it take end to end
    total_days = random.randint(1, 14)
    # Need a start date that lets the total days fit within valid days
    max_start_date_index = (len(valid_dates)-1) - total_days
    # Pick any of the valid start days
    start_date_index = random.randint(0, max_start_date_index)
    start_date = valid_dates[start_date_index]
    end_date = valid_dates[start_date_index+total_days]
    # Create a timestamp for each step in the selected path
    timestamps = generate_random_timestamps_range(
        start_date, end_date, steps)
    for i in range(0, steps):
        path_results.append({
            'status': valid_status[i],
            'status_updated_at': timestamps[i],
            'package_send_time': start_date,
            'package_deliv_time': end_date if i == steps-1 and valid_status[i] == 'delivered' else ''
        })

    return path_results


def generate_parcel_data(num_parcels):
    # Generate X number of parcel transactions, each with their complete end to end paths
    for parcel in range(0, num_parcels):
        sender_id = get_customer_id()
        package_id = str(uuid4())
        recv_id = str(uuid4())
        courier_id = random.choice(valid_couriers)
        for path in generate_parcel_path():
            yield {
                'sender_id': sender_id,
                'package_id': package_id,
                'recv_id': recv_id,
                'courier_id': courier_id,
                'status': path['status'],
                'status_updated_at': str(path['status_updated_at']),
                'package_send_time': str(path['package_send_time']),
                'package_deliv_time': str(path['package_deliv_time']),
            }