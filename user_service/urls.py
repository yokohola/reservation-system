from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from user_service import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('', include('rest_framework.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', ])
