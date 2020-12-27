from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api_loan'

router = routers.DefaultRouter()
router.register("api_loan", views.ApprovalsView)
urlpatterns = [
    # path('api/', include(router.urls)),
    # path('status/', views.approvereject),
    path('loan/', views.cxcontact, name="cxform")
]
