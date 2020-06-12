from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register("api_loan", views.ApprovalsView)
urlpatterns = [
    # path('api/', include(router.urls)),
    # path('status/', views.approvereject),
    path('loan/', views.cxcontact, name="cxform")
]
