from django.conf.urls import url
from website import views
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

urlpatterns = [
    url(r'^wex$', views.weixin_main),
    url(r'^login$', views.login),
    url(r'^test$', views.test),
    url(r'^get_all_user$', views.get_all_user),
    url(r'^get_data$', views.get_data),
]
