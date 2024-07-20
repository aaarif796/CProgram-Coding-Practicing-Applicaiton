
from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.question_list, name='question_list'),
#     path('<int:question_id>/', views.question_detail, name='question_detail'),
#     path('compile-and-run/', views.compile_and_run, name='compile_and_run'),
# ]

# from django.urls import path
# from . import views

app_name = 'Question'  # Capital Q for the app name

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('compile-and-run/', views.compile_and_run, name='compile_and_run'),
]