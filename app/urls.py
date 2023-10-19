from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process_selection/<int:customer_id>/', views.process_selection, name='process_selection'),
    path('measurement/<int:customer_id>/', views.measurement, name='measurement'),
    path('select_hinge/<int:customer_id>/', views.select_hinge, name='select_hinge'),
    path('lock-selection/<int:customer_id>/', views.lock_selection, name='lock_selection'),
    path('finish-selection/<int:customer_id>/', views.finish_selection, name='finish_selection'),
    path('door_open/<int:customer_id>/', views.door_open_selection, name='door_open_selection'),
    path('frame/<int:customer_id>/', views.frame_selection, name='frame_selection'),
    path('update_advance/<int:customer_id>/', views.update_advance_payment, name='update_advance_payment'),

    # ... other URL patterns ...


    # ... other URL patterns ...
]
