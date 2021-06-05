from django.contrib import admin
from django.urls import path, re_path
from wts.views import RedisView, ReadProject


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('companyWorkHoursSum', RedisView.as_view())
    re_path(r"^companyWorkHoursSum", RedisView.as_view()),
    re_path(r"^projectWorkHoursSum", ReadProject.as_view())
    # path('companyWorkHoursSum', RedisView.as_view())

]