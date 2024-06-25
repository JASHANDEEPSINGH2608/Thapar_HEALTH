# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




from django.contrib import admin
from django.urls import path

from FirstProject.views import home_view
#from FirstProject.views import about_view
# from FirstProject.views import product_detail_view
from FirstProject.views import login_view
from FirstProject.views import logout_view
from FirstProject.views import signup_view
from FirstProject.views import forgot_view
from FirstProject.views import change_view
from FirstProject.views import appointment_view
from FirstProject.views import userprofile_view
from FirstProject.views import doctor_view
from FirstProject.views import automate_google_meet
from FirstProject.views import history_view,patient_view
from FirstProject.views import prescription_upload
from django.contrib.auth import views as auth_views





urlpatterns = [
    # path('home2/', product_detail_view,),
    path('home/', home_view,name='home'),
   # path('about/', about_view,),
    path('admin/', admin.site.urls),
    path('', login_view, name='login_view'),
    path('logout/',logout_view, name='logout_view'),
    path('signup/',signup_view,name='signup_view'),
    path('forgot/',forgot_view,name='forgot_view'),
    path('change_password/<str:token>/', change_view, name='change_view'),
    path('appointment/',appointment_view,name='appointment_view'),
    path('userprofile/',userprofile_view,name='userprofile_view'),
    path('doctorview/',doctor_view,name='doctor_view'),
    path('google_meet/',automate_google_meet,name='google_meet'),
    path('History/',history_view,name='History_view'),
    path('prescription_upload/', prescription_upload, name='prescription_upload'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('patient/',patient_view,name='patient_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


