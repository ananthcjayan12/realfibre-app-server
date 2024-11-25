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
    path('doors/pdf/<int:customer_id>/', views.door_pdf_view, name='door_pdf'),
    path('update_customer_details/<int:customer_id>/', views.update_customer_details, name='update_customer_details'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer/<int:customer_id>/complete/', views.mark_as_complete, name='mark_as_complete'),
    path('customer/<int:customer_id>/show_pdf/', views.show_pdf, name='show_pdf'),
    path('customer/<int:customer_id>/update_balance/', views.update_balance, name='update_balance'),
     path('login/', views.CustomLoginView.as_view(), name='agent_login'),
    path('logout/', views.agent_logout, name='agent_logout'),
    path('create_agent/', views.create_agent, name='create_agent'),
    path('door_and_glass_selector/<int:door_id>/', views.door_and_glass_selector_view, name='door_and_glass_selector_view'),
    path('update_balance/', views.update_balance, name='update_balance'),
    path('update_priority/', views.update_priority, name='update_priority'),
    path('show-pdf-for-day/', views.show_pdf_for_day, name='show_pdf_for_day'),
    path('door_batch_dashboard/', views.door_batch_dashboard, name='door_batch_dashboard'),
    path('doorwise-dashboard/', views.doorwise_dashboard, name='doorwise_dashboard'),
    path('remarks/<int:door_id>/', views.remarks, name='remarks'),
     path('printpdf/<str:session_name>/', views.print_pdf, name='print_pdf'),
     path('printpdfmaterials/<str:session_name>/', views.print_pdf_materials, name='print_pdf_materials'),



    # ... other URL patterns ...


    # ... other URL patterns ...
]
