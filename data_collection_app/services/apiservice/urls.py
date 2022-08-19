from django.conf.urls import url
from .views import ApiViewSet
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('getImage' , ApiViewSet.as_view(
        {
            'get':'getImage'
        }
    )),
    path('getObject/<str:query>' , ApiViewSet.as_view(
        {
            'get':'getObject'
        }
    )),
    path('saveAnnoatations', ApiViewSet.as_view(
        {
            'post':'saveAnnoatations'
        }
    )),
    path('consent', ApiViewSet.as_view(
        {
            'post':'submitconsent'
        }
    )),
    # url(r'^getImage/$',views.getImage),
    # url(r'^getObject/$',views.getObject),
    # url(r'^saveAnnoatations',views.saveAnnoatations)
]