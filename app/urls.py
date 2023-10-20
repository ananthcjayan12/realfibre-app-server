from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process_selection/<int:door_id>/', views.process_selection, name='process_selection'),
    path('measurement/<int:door_id>/', views.measurement, name='measurement'),
    path('select_hinge/<int:door_id>/', views.select_hinge, name='select_hinge'),
    path('lock-selection/<int:door_id>/', views.lock_selection, name='lock_selection'),
    path('finish-selection/<int:door_id>/', views.finish_selection, name='finish_selection'),
    path('door_open/<int:door_id>/', views.door_open_selection, name='door_open_selection'),
    path('frame/<int:door_id>/', views.frame_selection, name='frame_selection'),
    path('update_advance/<int:door_id>/', views.update_advance_payment, name='update_advance_payment'),
     path('customer/<int:customer_id>/doors/', views.door_selection, name='door_selection'),
    path('door/<int:door_id>/delete/', views.delete_door, name='delete_door'),

    # ... other URL patterns ...


    # ... other URL patterns ...
]
