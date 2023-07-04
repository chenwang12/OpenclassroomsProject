from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.singnup),
    path('login/', views.login),
    path('projects/', views.projects),
    path('projects/<int:id>/', views.prj_detail),
    path('projects/<int:id>/users/', views.prj_users),
    path('projects/<int:id>/users/<int:id>', views.prj_user_info),
    path('projects/<int:id>/issues/', views.prj_issues),
    path('projects/<int:id>/issues/<int:id>', views.prj_issue_detail),
    path('projects/<int:id>/issues/<int:id>/comments/', views.prj_issue_comments),
    path('projects/<int:id>/issues<int:id>/comments/<int:id>', views.prj_issue_comment_info)
]