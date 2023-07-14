from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import json

# Create your models here.

class Users(AbstractBaseUser):
    class Meta:
        app_label = 'tracking'
        db_table = 'users'
    
    REQUIRED_FIELDS = ('password', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'

    user_id = models.IntegerField(auto_created=True, primary_key=True)
    first_name = models.CharField(max_length=20,null=False)
    last_name = models.CharField(max_length=20,null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, null=False)

    # @property
    # def is_anonymous(self):
    #     """
    #     Always return False. This is a way of comparing User objects to
    #     anonymous users.
    #     """
    #     return False
    
    # @property
    # def is_authenticated(self):
    #     """
    #     Always return False. This is a way of comparing User objects to
    #     anonymous users.
    #     """
    #     return False

    def __str__(self):
        return str(vars(self))


class Projects(models.Model):
    class Meta:
        app_label = "tracking"
        db_table = 'projects'

    REQUIRED_FIELDS = ('title','type')
    type_choices = [("back end","Back End"), ("front end","Font End"), ("iOS","IOS"),("Android","Android")]
    project_id = models.IntegerField(auto_created=True,primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=10,choices=type_choices)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


# class Contributors(models.Model):
#     """Represents a person having contributed to an issue. 
#     Contributors should be able to create or access issues in a project."""
#     class Meta:
#         permissions = [
#             ("view_issue", "Can view issue"),
#             ("create_issue", "Can create issue"),
#             ("modify_issue", "Can modify issue"),
#             ("delete_issue", "Can delete issue"),
#         ]
#     role_choices = (("author","Author"),("owner","Owner"),("creator","Creater"))
#     user_id = models.ForeignKey(Users,on_delete=models.CASCADE,to_field='user_id')
#     project_id = models.ForeignKey(Projects,on_delete=models.CASCADE,to_field='project_id')
#     # Define permission for roles
#     permission = models.BooleanField(default=True)
#     role = models.CharField(max_length=8,choices=role_choices)
    

# class Issues(models.Model):
#     tag_choices = (("bug","Bug"),("task","Task"),("enhancement","Enhancement"))
#     priority_choices = (("low","Low"),("medium","Medium"),("high","High"))
#     status_choices = (("To-Do","To Do"), ("In-Progress","In Progress"),("Completed","Completed"))
#     issue_id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=100,null=False)
#     desc = models.CharField(max_length=200,null=False)
#     tag = models.CharField(max_length=15,choices=tag_choices)
#     priority = models.CharField(max_length=8,choices=priority_choices)
#     project_id = models.ForeignKey(Projects,on_delete=models.CASCADE,to_field='project_id')
#     status = models.CharField(max_length=15)
#     author_user_id = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="author_id")
#     assignee_user_id = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="assignee_id")
#     create_tme = models.DateField(auto_now_add=True)

   
# class Comments(models.Model):
#     comment_id = models.IntegerField(primary_key=True)
#     description = models.TextField(max_length=255)
#     author_user_id = models.ForeignKey(Users,on_delete=models.CASCADE,to_field='user_id')
#     issue_id = models.ForeignKey(Issues,on_delete=models.CASCADE)
#     create_tme = models.DateField(auto_now_add=True)
    
