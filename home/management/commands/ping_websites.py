from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, time
import grequests


class Command(BaseCommand):
    help = 'Pings other Heroku sites to keep them awake'
    SLEEP_TIME = time(22, 0)
    WAKE_TIME = time(6, 0)
    urls = [
        'https://fplmanager.herokuapp.com',
        'https://tracklistify.herokuapp.com',
    ]

    def handle(self, *args, **options):
        if not self.active:
            return
        self.async_get()

    @property
    def active(self):
        t_now = datetime.now().time()
        if self.WAKE_TIME < self.SLEEP_TIME:
            return t_now > self.WAKE_TIME and t_now < self.SLEEP_TIME
        else:  # sleep period crosses midnight
            return t_now > self.WAKE_TIME or t_now < self.SLEEP_TIME

    def _async_get_exception(self, request, exception):
        self.stdout.write("Problem: {}: {}".format(request.url, exception))

    def async_get(self):
        reqs = (grequests.get(u) for u in self.urls)
        r = grequests.map(reqs, exception_handler=self._async_get_exception)
        self.stdout.write(r)