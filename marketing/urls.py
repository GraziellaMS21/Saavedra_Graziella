# # marketing/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.predict_view, name='predict'),
# ]


# with db
# marketing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # Homepage is now the table
    path('predict/', views.predict_view, name='predict'), # Create new
    path('predict/<int:pk>/edit/', views.predict_view, name='edit_predict'), # Edit existing
    path('predict/<int:pk>/result/', views.result_view, name='result'), # View result
    path('predict/<int:pk>/delete/', views.delete_view, name='delete_predict'), # Delete
]