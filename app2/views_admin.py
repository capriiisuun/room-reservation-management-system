from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Salle, Equipement, Reservation, EquipementExterne,DroitAcces
from .forms import (SalleForm, EquipementForm,CustomUserCreationForm, UtilisateurForm,ReservationAdminForm,DroitAccesForm)

User = get_user_model()

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def salle_list(request):
    salles = Salle.objects.all()
    return render(request, 'app2/admin/salle_list.html', {'salles': salles})

@login_required
@user_passes_test(is_admin)
def salle_create(request):
    if request.method == 'POST':
        form = SalleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_salle_list')
    else:
        form = SalleForm()
    return render(request, 'app2/admin/salle_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def salle_update(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        form = SalleForm(request.POST, request.FILES, instance=salle)
        if form.is_valid():
            form.save()
            return redirect('gestion_salle_list')
    else:
        form = SalleForm(instance=salle)
    return render(request, 'app2/admin/salle_form.html', {'form': form, 'salle': salle})

@login_required
@user_passes_test(is_admin)
def salle_delete(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        salle.delete()
        return redirect('gestion_salle_list')
    return render(request, 'app2/admin/salle_confirm_delete.html', {'salle': salle})

@login_required
@user_passes_test(is_admin)
def equipement_list(request):
    equipements = Equipement.objects.select_related('salle').all()
    return render(request, 'app2/admin/equipement_list.html', {'equipements': equipements})

@login_required
@user_passes_test(is_admin)
def equipement_create(request):
    if request.method == 'POST':
        form = EquipementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_equipement_list')
    else:
        form = EquipementForm()
    return render(request, 'app2/admin/equipement_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def equipement_update(request, pk):
    eq = get_object_or_404(Equipement, pk=pk)
    if request.method == 'POST':
        form = EquipementForm(request.POST, instance=eq)
        if form.is_valid():
            form.save()
            return redirect('gestion_equipement_list')
    else:
        form = EquipementForm(instance=eq)
    return render(request, 'app2/admin/equipement_form.html', {'form': form, 'equipement': eq})

@login_required
@user_passes_test(is_admin)
def equipement_delete(request, pk):
    eq = get_object_or_404(Equipement, pk=pk)
    if request.method == 'POST':
        eq.delete()
        return redirect('gestion_equipement_list')
    return render(request, 'app2/admin/equipement_confirm_delete.html', {'equipement': eq})


@login_required
@user_passes_test(is_admin)
def utilisateur_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'app2/admin/utilisateur_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def utilisateur_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Utilisateur '{user.username}' créé !")
            return redirect('gestion_utilisateur_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app2/admin/utilisateur_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def utilisateur_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Utilisateur '{user.username}' modifié !")
            return redirect('gestion_utilisateur_list')
    else:
        form = UtilisateurForm(instance=user)
    return render(request, 'app2/admin/utilisateur_form.html', {'form': form, 'utilisateur': user})

@login_required
@user_passes_test(is_admin)
def utilisateur_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"Utilisateur '{username}' supprimé !")
        return redirect('gestion_utilisateur_list')
    return render(request, 'app2/admin/utilisateur_confirm_delete.html', {'utilisateur': user})

@login_required
@user_passes_test(is_admin)
def reservation_list(request):
    reservations = Reservation.objects.select_related('utilisateur', 'salle', 'creneau').all().order_by('-date_debut')
    return render(request, 'app2/admin/reservation_list.html', {'reservations': reservations})

@login_required
@user_passes_test(is_admin)
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationAdminForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.save()
            # Affectation des équipements externes sélectionnés
            for ext in form.cleaned_data.get('equipements_externes', []):
                ext.reservation = reservation
                ext.save()
            messages.success(request, "Réservation créée !")
            return redirect('gestion_reservation_list')
    else:
        form = ReservationAdminForm()
    return render(request, 'app2/admin/reservation_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationAdminForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.save()
            # Détachement des anciens équipements externes
            EquipementExterne.objects.filter(reservation=reservation).update(reservation=None)
            # Réaffectation des sélectionnés
            for ext in form.cleaned_data.get('equipements_externes', []):
                ext.reservation = reservation
                ext.save()
            messages.success(request, "Réservation mise à jour !")
            return redirect('gestion_reservation_list')
    else:
        form = ReservationAdminForm(instance=reservation)
    return render(request, 'app2/admin/reservation_form.html', {'form': form, 'reservation': reservation})

@login_required
@user_passes_test(is_admin)
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Réservation supprimée !")
        return redirect('gestion_reservation_list')
    return render(request, 'app2/admin/reservation_confirm_delete.html', {'reservation': reservation})
from .models import CategorieSalle
from .forms import CategorieSalleForm

@login_required
@user_passes_test(is_admin)
def categorie_list(request):
    categories = CategorieSalle.objects.all().order_by('nom')
    return render(request, 'app2/admin/categorie_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def categorie_create(request):
    if request.method == 'POST':
        form = CategorieSalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_categorie_list')
    else:
        form = CategorieSalleForm()
    return render(request, 'app2/admin/categorie_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def categorie_update(request, pk):
    categorie = get_object_or_404(CategorieSalle, pk=pk)
    if request.method == 'POST':
        form = CategorieSalleForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('gestion_categorie_list')
    else:
        form = CategorieSalleForm(instance=categorie)
    return render(request, 'app2/admin/categorie_form.html', {'form': form, 'categorie': categorie})

@login_required
@user_passes_test(is_admin)
def categorie_delete(request, pk):
    categorie = get_object_or_404(CategorieSalle, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('gestion_categorie_list')
    return render(request, 'app2/admin/categorie_confirm_delete.html', {'categorie': categorie})


@login_required
@user_passes_test(is_admin)
def droitacces_list(request):
    droits = DroitAcces.objects.select_related('utilisateur').all().order_by('utilisateur__username')
    return render(request, 'app2/admin/droitacces_list.html', {'droits': droits})

@login_required
@user_passes_test(is_admin)
def droitacces_create(request):
    if request.method == 'POST':
        form = DroitAccesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_droitacces_list')
    else:
        form = DroitAccesForm()
    return render(request, 'app2/admin/droitacces_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def droitacces_update(request, pk):
    droit = get_object_or_404(DroitAcces, pk=pk)
    if request.method == 'POST':
        form = DroitAccesForm(request.POST, instance=droit)
        if form.is_valid():
            form.save()
            return redirect('gestion_droitacces_list')
    else:
        form = DroitAccesForm(instance=droit)
    return render(request, 'app2/admin/droitacces_form.html', {'form': form, 'droit': droit})

@login_required
@user_passes_test(is_admin)
def droitacces_delete(request, pk):
    droit = get_object_or_404(DroitAcces, pk=pk)
    if request.method == 'POST':
        droit.delete()
        return redirect('gestion_droitacces_list')
    return render(request, 'app2/admin/droitacces_confirm_delete.html', {'droit': droit})
