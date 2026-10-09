from django.db import models
from django.contrib.auth.models import User;
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class CategorieSalle(models.Model):
    nom = models.CharField(max_length=100)
    type_salle = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} - {self.type_salle}"

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacite = models.IntegerField()
    description = models.TextField()
    categorie = models.ForeignKey(CategorieSalle, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='salles/', null=True, blank=True)

    def __str__(self):
        return self.nom





class Equipement(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='equipements')
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom


class DroitAcces(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_droit = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.type_droit}"


class Creneau(models.Model):
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.heure_debut.strftime('%H:%M')} - {self.heure_fin.strftime('%H:%M')}"


class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.salle.nom} - {self.date_debut.date()}"
    

class EquipementExterne(models.Model):
    nom   = models.CharField(max_length=100)
    description = models.TextField()
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='equipements_externes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom


class Calendrier(models.Model):

    @staticmethod
    def imprimer_par_salle(salle_id):
        return Reservation.objects.filter(salle_id=salle_id)

    @staticmethod
    def imprimer_par_semaine(date_reference):
        from datetime import timedelta
        semaine_debut = date_reference - timedelta(days=date_reference.weekday())
        semaine_fin = semaine_debut + timedelta(days=6)
        return Reservation.objects.filter(date_debut__date__range=[semaine_debut, semaine_fin]) 
