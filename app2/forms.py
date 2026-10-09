from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import CategorieSalle,DroitAcces
from .models import (Utilisateur, Salle, Equipement,Reservation, EquipementExterne,)



class CategorieSalleForm(forms.ModelForm):
    class Meta:
        model = CategorieSalle
        fields = ['nom', 'type_salle']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type_salle': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ReservationAdminForm(forms.ModelForm):
    equipements_externes = forms.ModelMultipleChoiceField(
        queryset=EquipementExterne.objects.filter(reservation__isnull=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Équipements externes"
    )

    class Meta:
        model = Reservation
        fields = [
            'utilisateur', 'salle', 'creneau',
            'date_debut', 'date_fin', 'statut',
            'equipements_externes'
        ]
        widgets = {
            'utilisateur': forms.Select(attrs={'class':'form-control'}),
            'salle':forms.Select(attrs={'class':'form-control'}),
            'creneau':forms.Select(attrs={'class':'form-control'}),
            'date_debut':forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'date_fin':forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'statut':forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # en édition, conserver les externes déjà liés
        if self.instance.pk:
            self.fields['equipements_externes'].queryset = (
                EquipementExterne.objects
                                .filter(reservation__isnull=True)
                                .union(self.instance.equipements_externes.all())
            )

class UtilisateurForm(UserChangeForm):
    password = None  

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'role', 'is_staff', 'is_active']
        widgets = {
            'username':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'role':forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'password1', 'password2')


class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite', 'categorie', 'description', 'image']
        widgets = {
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'capacite':forms.NumberInput(attrs={'class': 'form-control'}),
            'categorie':forms.Select(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'image':forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = ['salle', 'nom', 'description']
        widgets = {
            'salle':forms.Select(attrs={'class': 'form-control'}),
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }


class DroitAccesForm(forms.ModelForm):
    class Meta:
        model = DroitAcces
        fields = ['utilisateur', 'type_droit']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-control'}),
            'type_droit':  forms.TextInput(attrs={'class': 'form-control'}),
        }
