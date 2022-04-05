from django.db import models
from django.utils.crypto import get_random_string
from uuid import uuid4


class Room(models.Model):
    name = models.CharField(max_length=8, unique=True)
    num_users = models.IntegerField(default=1)
    user_uuid = models.UUIDField(default=uuid4)
    is_open = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            while Room.objects.filter(name=self.name).exists() or not self.name:
                self.name = get_random_string(8)

        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)
