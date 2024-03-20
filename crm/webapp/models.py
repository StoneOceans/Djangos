from django.db import models
from django.utils import timezone

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    province = models.CharField(max_length=200)

    country = models.CharField(max_length=125)


    def __str__(self):

        return self.first_name + "   " + self.last_name


class Fichier(models.Model):
    nom = models.CharField(max_length=100)
    contenu = models.FileField(upload_to='fichiers/')
    temps = models.DateTimeField(default=timezone.now)


class Redevance(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    flpl_call_sign = models.CharField(max_length=9)

    flpl_depr_airp = models.CharField(max_length=4)

    flpl_arrv_airp = models.CharField(max_length=4)

    airc_type = models.CharField(max_length=25)

    aobt = models.IntegerField()

    eobt = models.IntegerField(default=1)

    file_date = models.IntegerField(default=1)  # Add default 0

    flight_state = models.CharField(max_length=25, default=1)

    flight_type = models.CharField(max_length=25, default=1)

    ifps_registration_mark = models.CharField(max_length=25, default=1)

    initial_flight_rule = models.CharField(max_length=25, default=1)

    nm_ifps_id = models.CharField(max_length=25, default=1)

    nm_tactical_id = models.IntegerField(default=1)


 







