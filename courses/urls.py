from django.urls import path
from . import views

urlpatterns = [
    path('', views.browse_courses, name='browse_courses'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>', views.enroll_course, name='enroll_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('<int:course_id>/upload/', views.upload_material, name='upload_material'),
    path("material/<int:course_id>/download/", views.download_material, name="download_material"),
    path('block/<int:student_id>/<int:course_id>/', views.block_student, name='block_student'),
    path("unblock/<int:student_id>/<int:course_id>/", views.unblock_student, name="unblock_student"),
    path('<int:course_id>/chat/', views.course_chat, name='course_chat'),
]