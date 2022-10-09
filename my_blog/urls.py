from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

router.register('Tag',views.UserProfileTagsViewSet)
router.register('Posts',views.UserProfilePostsViewSet)
router.register('Profile',views.UserProfileViewSet)

#router.register('password_reset/',include('django_rest_passwordreset.urls', namespace='password_reset'))

urlpatterns = [
    path('',include(router.urls)),
    path('login/',views.userloginapiview.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('posts/<slug:slug>',),#it checks if concrete calue consists of slug : has numbers and dasha and alphabet
    
]
