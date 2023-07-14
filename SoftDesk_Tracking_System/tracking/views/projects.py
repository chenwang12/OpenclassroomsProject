#from django.contrib.auth.decorators import login_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from django.db.utils import IntegrityError
import json
from tracking import models

#---------------BEGIN /projects/----------------
def getProjects(request):
    print(request)
    print(request.user)
    print(request.META)

    projects = models.Projects.objects.all()
    print(projects)
    data = serializers.serialize('json',projects)
    return JsonResponse(json.loads(data),safe=False,status=200)
    
def createProject(request):
    body = None
    try:
        #if POST in request:
        # body = request.POST
        # else:
        # request.body = json.dumps(request.POST)
        body = json.loads(request.body)
    except:
        error = { "message": f"error parsing JSON {request.body}" }
        return JsonResponse(error, status=400)
    
    try:
        #TODO: get actual user logged in
        user = models.Users.objects.get(user_id=2)
        body['author_user_id'] = user
        newAccount = models.Projects(**body)
        newAccount.save()
    except IntegrityError as e:
        print(e)
        error = { "message": f"project {body['title']} already exits" }
        return JsonResponse(error, status=409)
    except Exception as e:
        print(e)
        print(type(e))
        error = { "message": f"problem creating project {body['title']}" }
        return JsonResponse(error, status=500)
    
    data = { 
        "message": f"project {body['title']} created successfully"
     }
    return JsonResponse(data, safe=False, status=201)

projectsHandler = {
    'GET': getProjects,
    'POST': createProject
}

def handleProject(request):
    allowedMethods = ['GET', 'POST']
    if not request.method in allowedMethods:
        error = { "message": "invalid HTTP method" }
        return JsonResponse(error, status=405)
    
    return projectsHandler[request.method](request)

#-----------------END /projects/---------------------