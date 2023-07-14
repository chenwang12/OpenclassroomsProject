from django.urls import path
from tracking.views import users,projects

#app_label = "tracking"

urlpatterns = [
    # path("", views.index, name="index"),
    path('signup/', users.signup),
    path('login/', users.login),
    path('projects/', projects.handleProject),
    # path('projects/<int:id>/', views.prj_detail),
    # path('projects/<int:id>/users/', views.prj_users),
    # path('projects/<int:id>/users/<int:id>', views.prj_user_info),
    # path('projects/<int:id>/issues/', views.prj_issues),
    # path('projects/<int:id>/issues/<int:id>', views.prj_issue_detail),
    # path('projects/<int:id>/issues/<int:id>/comments/', views.prj_issue_comments),
    # path('projects/<int:id>/issues<int:id>/comments/<int:id>', views.prj_issue_comment_info)
]