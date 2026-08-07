from django.contrib import admin
from django.urls import path, include
from agendamentos.views import landing_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='home'),
    path('api/', include('servicos.urls')),
    path('api/', include('agendamentos.urls')),

]