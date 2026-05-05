import os
import random
from datetime import datetime

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django import setup

setup()
from authentication.models import User
from table.models import Table
from reservation.models import Reservation

fake = Faker()


def add_user(faker: Faker) -> User:
    return User.objects.create_user(
        username=faker.user_name(),
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        password=faker.password(length=12), )


def add_table(faker: Faker, number_table: int, available_photos: list[...]) -> Table:
    random_photo = random.choice(available_photos)
    photo_path = os.path.join('table_image', random_photo)
    return Table.objects.create(
        number=number_table,
        seats=random.randint(1, 10),
        description=fake.sentence(nb_words=7),
        image=photo_path,

    )


def add_reservation(faker: Faker, user: User, table: Table, date, hour_start: int,
                  hour_end: int) -> Reservation:
    return Reservation.objects.create(
        table=table,
        user=user,
        date=date,
        created_at=datetime.now(),
        hour_start=hour_start,
        hour_end=hour_end,

    )


def generate(faker: Faker):
    # users = []
    # for _ in range(10):
    #     users.append(add_user(faker))
    # available_photos = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
    # tables = []
    # for i in range(30):
    #     tables.append(add_table(faker, i, available_photos))
    #     print(".", end="")
    tables = Table.objects.all()
    users = User.objects.filter(username = "admin")
    for user in users:
        for _ in range(5000):
            table = random.choice(tables)
            date = faker.date_this_year(before_today=False, after_today=True)
            if Reservation.objects.filter(table=table, date = date).exists():
                continue
            hour_start = random.randint(8, 17)
            difference = random.randint(1,18-hour_start)
            hour_end = hour_start + difference
            if Reservation.objects.filter(
                    table=table,
                    date=date,
                    hour_start__lt=hour_end,
                    hour_end__gt=hour_start
            ).exists():
                continue
            add_reservation(faker, user, table, date, hour_start, hour_end)
            if _ % 50 == 0:
                print(".", end="")

#
def main() -> None:
    faker = Faker("ru_RU")
    generate(faker)


if __name__ == '__main__':
    main()
