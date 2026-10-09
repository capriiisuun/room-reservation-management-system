from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_admin

urlpatterns = [
   
    path('inscription/', views.inscription, name='inscription'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='accueil'),name='logout'),

    path('', views.accueil, name='accueil'),
    path('salles/',views.liste_salles,name='liste_salles'),
    path('recherche/',views.recherche_salles, name='recherche_salles'),
    path('calendrier/',views.imprimer_calendrier, name='imprimer_calendrier'),

    path('reserver/<int:salle_id>/',views.reserver_salle,name='reserver_salle'),
    path('mes_reservations/',views.mes_reservations,name='mes_reservations'),
    path('reservation/<int:reservation_id>/', views.detail_reservation, name='detail_reservation'),
    path('reservation/<int:reservation_id>/annuler/',views.annuler_reservation, name='annuler_reservation'),

    
    path('gestion/salles/',views_admin.salle_list,name='gestion_salle_list'),
    path('gestion/salles/add/',views_admin.salle_create, name='gestion_salle_create'),
    path('gestion/salles/<int:pk>/edit/',views_admin.salle_update, name='gestion_salle_update'),
    path('gestion/salles/<int:pk>/delete/',views_admin.salle_delete, name='gestion_salle_delete'),

    path('gestion/equipements/', views_admin.equipement_list,name='gestion_equipement_list'),
    path('gestion/equipements/add/',views_admin.equipement_create, name='gestion_equipement_create'),
    path('gestion/equipements/<int:pk>/edit/',views_admin.equipement_update, name='gestion_equipement_update'),
    path('gestion/equipements/<int:pk>/delete/',views_admin.equipement_delete, name='gestion_equipement_delete'),

path('gestion/utilisateurs/',views_admin.utilisateur_list,   name='gestion_utilisateur_list'),
path('gestion/utilisateurs/add/',views_admin.utilisateur_create, name='gestion_utilisateur_create'),
path('gestion/utilisateurs/<int:pk>/edit/',views_admin.utilisateur_update, name='gestion_utilisateur_update'),
path('gestion/utilisateurs/<int:pk>/delete/',views_admin.utilisateur_delete, name='gestion_utilisateur_delete'),

path('gestion/reservations/',views_admin.reservation_list,name='gestion_reservation_list'),
path('gestion/reservations/add/',views_admin.reservation_create, name='gestion_reservation_create'),
path('gestion/reservations/<int:pk>/edit/',views_admin.reservation_update, name='gestion_reservation_update'),
path('gestion/reservations/<int:pk>/delete/',views_admin.reservation_delete, name='gestion_reservation_delete'),

path('gestion/categories/',views_admin.categorie_list,   name='gestion_categorie_list'),
path('gestion/categories/add/',views_admin.categorie_create, name='gestion_categorie_create'),
path('gestion/categories/<int:pk>/edit/',views_admin.categorie_update, name='gestion_categorie_update'),
path('gestion/categories/<int:pk>/delete/',views_admin.categorie_delete, name='gestion_categorie_delete'),

path('gestion/droits/',views_admin.droitacces_list,name='gestion_droitacces_list'),
path('gestion/droits/add/',views_admin.droitacces_create, name='gestion_droitacces_create'),
path('gestion/droits/<int:pk>/edit/',views_admin.droitacces_update, name='gestion_droitacces_update'),
path('gestion/droits/<int:pk>/delete/',views_admin.droitacces_delete, name='gestion_droitacces_delete'),


]
