from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils  import timezone
from django.contrib    import messages
from datetime   import datetime, timedelta
from .models    import (Salle, Reservation, Creneau,EquipementExterne,CategorieSalle)
from .forms  import CustomUserCreationForm


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def accueil(request):
    categories = CategorieSalle.objects.prefetch_related('salle_set__equipements').all()
    return render(request, 'app2/accueil.html', {'categories': categories})


def liste_salles(request):
    categories = CategorieSalle.objects.prefetch_related('salle_set').all()
    return render(request, 'app2/liste_salles.html', {'categories': categories})

@login_required
def reserver_salle(request, salle_id):
    salle= get_object_or_404(Salle, id=salle_id)
    creneaux= Creneau.objects.all()
    today= timezone.now().date()
    available_ext_eqs = EquipementExterne.objects.filter(reservation__isnull=True)
    initial_date= request.GET.get('date', today.strftime('%Y-%m-%d'))
    initial_creneau = request.GET.get('creneau', '')

    if request.method == 'POST':
        date_str   = request.POST.get('date')
        creneau_id = request.POST.get('creneau')
        chosen_ids = request.POST.getlist('equipements_externes')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            creneau  = get_object_or_404(Creneau, id=creneau_id)
           
            conflict = Reservation.objects.filter(
                salle=salle,
                creneau=creneau,
                date_debut__date=date_obj,
                statut__in=['En attente', 'Confirmée']
            )
            if conflict.exists():
                messages.error(request, "Cette salle est déjà réservée pour ce créneau.")
            else:
                debut = datetime.combine(date_obj, creneau.heure_debut)
                fin   = datetime.combine(date_obj, creneau.heure_fin)
                reservation = Reservation.objects.create(
                    utilisateur=request.user,
                    salle=salle,
                    creneau=creneau,
                    date_debut=debut,
                    date_fin=fin,
                    statut="En attente"
                )
                if chosen_ids:
                    EquipementExterne.objects.filter(id__in=chosen_ids).update(reservation=reservation)
                messages.success(request, "Réservation enregistrée avec succès !")
                return redirect('mes_reservations')
        except Exception as e:
            messages.error(request, f"Erreur lors de la réservation : {e}")

    return render(request, 'app2/reserver_salle.html', {
        'salle': salle,
        'creneaux': creneaux,
        'today': today,
        'initial_date': initial_date,
        'initial_creneau': initial_creneau,
        'available_ext_eqs': available_ext_eqs,
    })

@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user).order_by('-date_debut')
    return render(request, 'app2/mes_reservations.html', {'reservations': reservations})

@login_required
def detail_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    return render(request, 'app2/detail_reservation.html', {'reservation': reservation})

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    if reservation.statut == 'Annulée':
        messages.error(request, "Cette réservation est déjà annulée.")
        return redirect('mes_reservations')
    if request.method == 'POST':
        reservation.statut = 'Annulée'
        reservation.save()
        messages.success(request, "Votre réservation a été annulée avec succès.")
        return redirect('mes_reservations')
    return render(request, 'app2/confirmer_annulation.html', {'reservation': reservation})

@login_required
def recherche_salles(request):
    today= timezone.now().date()
    creneaux  = Creneau.objects.all()
    categories = CategorieSalle.objects.all()
    query = Salle.objects.all()
    date_str= request.GET.get('date')
    creneau_id = request.GET.get('creneau')
    capacite= request.GET.get('capacite')
    cat_id= request.GET.get('categorie')

    if capacite:
        query = query.filter(capacite__gte=int(capacite))
    if cat_id:
        query = query.filter(categorie_id=cat_id)
    if date_str and creneau_id:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        booked = Reservation.objects.filter(
            date_debut__date=date_obj,
            creneau_id=creneau_id,
            statut__in=['En attente', 'Confirmée']
        ).values_list('salle_id', flat=True)
        query = query.exclude(id__in=booked)

    return render(request, 'app2/recherche.html', {
        'today': today,
        'creneaux': creneaux,
        'categories': categories,
        'salles': query,
    })

@login_required
def imprimer_calendrier(request):
    type_affichage = request.GET.get('type', 'semaine')
    date_str= request.GET.get('date')
    salle_id= request.GET.get('salle')
    if date_str:
        date_reference = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_reference = timezone.now().date()

    debut_semaine = date_reference - timedelta(days=date_reference.weekday())
    fin_semaine   = debut_semaine + timedelta(days=6)

    jours_semaine = [
        (['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'][i], debut_semaine + timedelta(days=i))
        for i in range(7)
    ]

    creneaux= Creneau.objects.all().order_by('heure_debut')
    salles= Salle.objects.all()
    reservations = Reservation.objects.filter(
        utilisateur=request.user,
        date_debut__date__range=[debut_semaine, fin_semaine]
    ).select_related('salle','creneau')

    salle_sel = None
    if salle_id:
        salle_sel = get_object_or_404(Salle, id=salle_id)
    
    return render(request, 'app2/imprimer_calendrier.html', {
        'type': type_affichage,
        'date': date_reference,
        'debut_semaine': debut_semaine,
        'fin_semaine': fin_semaine,
        'jours_semaine': jours_semaine,
        'creneaux': creneaux,
        'salles': salles,
        'reservations': reservations,
        'salle_id': salle_id,
        'salle_selectionnee': salle_sel,
    })
