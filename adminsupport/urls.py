from django.urls import path
from .views.EmployeeView import FetchADACEmployeeDataFullLoad
from .views.TimeAttendanceReport import UploadTimeAttendanceReport, FetchTimeAttendaceReport, FetchUniqueColumns

urlpatterns = [
    path('fetch-employee-full-load/', FetchADACEmployeeDataFullLoad.as_view(),
         name='fetch-employee-full-load'),
    path('upload-ta-report/', UploadTimeAttendanceReport.as_view(),
         name='upload-ta-report'),
    path('fetch-ta-report/', FetchTimeAttendaceReport.as_view(),
         name='fetch-ta-report'),
    path('fetch-disticnt-cols/', FetchUniqueColumns.as_view(),
         name='fetch-disticnt-cols')
]
