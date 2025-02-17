from django.db import models
from django.urls import reverse

class Meal(models.Model):
    name = models.CharField(max_length=200)
    kcal = models.DecimalField(max_digits=6, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.kcal} </a>'
