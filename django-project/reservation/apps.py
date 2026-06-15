from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class ReservationConfig(AppConfig):
    name = 'reservation'

    def ready(self):
        from .services import MyNotesCache
        from reservation.models import Reservation
        def post_save_reservation_signal(sender, instance, created, **kwargs):
            if created:
                MyNotesCache.clear_cache()

        def post_delete_reservation_signal(sender, instance, **kwargs):
            MyNotesCache.clear_cache()

        post_save.connect(post_save_reservation_signal, sender=Reservation, weak=False,
                          dispatch_uid='post_save_reservation_signal')
        post_delete.connect(post_delete_reservation_signal, sender=Reservation, weak=False,
                            dispatch_uid='post_delete_reservation_signal')
