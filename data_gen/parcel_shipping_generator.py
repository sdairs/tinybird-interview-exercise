import random
import datetime
from tracemalloc import start
from uuid import uuid4

valid_paths = {
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
valid_paths_weights = [80, 2, 15, 3]

parcels = {}


class Parcel():

    status_index = 0
    status_index_max = None
    created_datetime = None
    date_for_next_update = None
    path = None

    data = {
        'sender_id': str(uuid4()),
        'package_id': str(uuid4()),
        'recv_id': str(uuid4()),
        'courier_id': str(uuid4()),
        'status': None,
        'status_updated_at': None,
        'package_send_time': None,
        'package_deliv_time': None
    }

    def date(self):
        return self.date_for_next_update.date()

    def __init__(self, created_datetime):
        self.path = random.choices(list(valid_paths.keys()),
                                   weights=valid_paths_weights, k=1)[0]
        self.data['status'] = valid_paths[self.path][0]
        self.data['package_send_time'] = str(created_datetime)
        self.data['status_updated_at'] = str(created_datetime)
        self.status_index_max = len(valid_paths[self.path])-1
        self.created_datetime = created_datetime
        self.date_for_next_update = self.generate_random_future_timestamp(
            self.created_datetime, 4)

    def generate_random_future_timestamp(self, current_date, max_future_days=7) -> datetime:
        future_day = random.randint(1, max_future_days)
        future_hour = random.randint(1, 24)
        future_minute = random.randint(1, 60)
        future_datetime = current_date + \
            datetime.timedelta(
                days=future_day, hours=future_hour, minutes=future_minute)
        return future_datetime

    def is_complete(self):
        return True if self.status_index == self.status_index_max else False

    def update_status(self) -> bool:
        # Returns False if the status was updated, but the parcel is not complete
        # Returns True is the status was updated, and the parcel is now complete
        self.status_index += 1
        self.data['status'] = valid_paths[self.path][self.status_index]
        self.data['status_updated_at'] = str(self.date_for_next_update)
        if self.is_complete():
            self.date_for_next_update = None
            return True
        else:
            self.date_for_next_update = self.generate_random_future_timestamp(
                self.date_for_next_update, 4)
            return False


def add_parcel(parcel):
    try:
        parcels[parcel.date()].append(parcel)
    except KeyError:
        parcels[parcel.date()] = [parcel]


def generate_parcel_data(max_days=100, parcels_per_day=1000):
    starting_date = datetime.datetime.today() - datetime.timedelta(days=max_days)
    for day in range(0, max_days):
        # LOOP: Iterating over the days in scope
        today = starting_date + datetime.timedelta(days=day)
        print(
            f'Working on day {day} with date {today.year}-{today.month}-{today.day}')
        for _ in range(1, parcels_per_day):
            # LOOP: Iterating over the parcels to create today
            parcel = Parcel(created_datetime=today)
            add_parcel(parcel)
        if today.date() in parcels:
            parcels_to_update_today = len(parcels[today.date()])
            print(f'There are {parcels_to_update_today} to update today.')
            for parcel in parcels[today.date()]:
                # LOOP: Iterate over todays parcels, yield the parcel's data if complete
                if not parcel.update_status():
                    add_parcel(parcel)
                else:
                    yield parcel.data
            del parcels[today.date()]
