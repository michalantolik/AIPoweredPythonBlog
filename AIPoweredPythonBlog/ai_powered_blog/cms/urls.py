from django.urls import path

from .views import plantuml_svg

app_name = "cms"

urlpatterns = [
    path("svg/<str:diagram_id>/", plantuml_svg, name="plantuml_svg"),
]
