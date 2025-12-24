from django.urls import path , include
from home.views import loginAPI,RegistrationAPI , ProductModelViewSet ,OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'myproduct',ProductModelViewSet,basename = 'myproduct')
urlpatterns = router.urls 

router2 = DefaultRouter()
router2.register(r'myorders',OrderViewSet,basename = 'myorders')
urlpatterns = router2.urls 


urlpatterns = [
    path('myorders/',include(router2.urls)),
    path('myproduct/',include(router.urls)),
    path('register/',RegistrationAPI.as_view(),name = 'register'),
    path('login/',loginAPI.as_view(),name='login'),
    #path('api/',include('rest_API.urls')),

]
