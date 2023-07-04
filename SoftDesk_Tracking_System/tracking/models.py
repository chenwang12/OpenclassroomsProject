from django.db import models

# Create your models here.

class Users(models.Model):
    
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(null=False)
    last_name = models.CharField(null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  
    def __str__(self):
        return f'{self.user_id} ({self.last_name},{self.first_name})'


class Projects(models.Model):
    type_choices = [("back end","Back End"), ("front end","Font End"), ("iOS","IOS"),("Android","Android")]
    project_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(choices=type_choices)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Contributors(models.Model):
    """Represents a person having contributed to an issue. 
    Contributors should be able to create or access issues in a project."""
    class Meta:
        permissions = [
            ("view_issue", "Can view issue"),
            ("create_issue", "Can create issue"),
            ("modify_issue", "Can modify issue"),
            ("delete_issue", "Can delete issue"),
        ]
    role_choices = (("author","Author"),("owner","Owner"),("creator","Creater"))
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE,to_field='user_id')
    project_id = models.ForeignKey(Projects,on_delete=models.CASCADE,to_field='project_id')
    # Define permission for roles
    permission = models.BooleanField(default=True)
    role = models.CharField(choices=role_choices)
    

class Issues(models.Model):
    tag_choices = (("bug","Bug"),("task","Task"),("enhancement","Enhancement"))
    priority_choices = (("low","Low"),("medium","Medium"),("high","High"))
    status_choices = (("To-Do","To Do"), ("In-Progress","In Progress"),("Completed","Completed"))
    issue_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100,null=False)
    desc = models.CharField(max_length=255,null=False)
    tag = models.CharField(choices=tag_choices)
    priority = models.CharField(choices=priority_choices)
    project_id = models.ForeignKey(Projects,on_delete=models.CASCADE,to_field='project_id')
    status = models.CharField(max_length=100)
    author_user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey("Assignee",Users,on_delete=models.CASCADE)
    create_tme = models.DateField("Date Created",auto_now_add=True)

   
class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=255)
    author_user_id = models.ForeignKey(Users,on_delete=models.CASCADE,to_field='user_id')
    issue_id = models.ForeignKey(Issues,on_delete=models.CASCADE)
    create_tme = models.DateField(auto_now_add=True)
    
