from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

# router.register('Tag',)
# router.register('Posts',)
# router.register('Profile',)

urlpatterns = [
    # path('',include(router.urls)),
    # path('posts/',),
    # path('posts/<slug:slug>',),#it checks if concrete calue consists of slug : has numbers and dasha and alphabet
    
]
