#from django.contrib.auth.decorators import login_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
import json
from tracking import models

# def create_view(request):
#     if request.method == 'POST':
#         form = MyModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:detail', pk=form.instance.pk)
#     else:
#         form = MyModelForm()
#     return render(request, 'myapp/create.html', {'form': form})

#@login_exempt
def signup(request):
    if request.method != 'POST':
        error = { "message": "only POST is allowed" }
        return JsonResponse(error, status=405)
    
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
        newAccount = models.Users(**body)
        newAccount.save()
    except IntegrityError:
        error = { "message": f"user {body['email']} already exits" }
        return JsonResponse(error, status=409)
    except Exception as e:
        print(e)
        print(type(e))
        error = { "message": f"problem creating user {body['email']}" }
        return JsonResponse(error, status=500)
    
    data = { 
        "message": f"user {body['email']} created successfully"
     }
    return JsonResponse(data, safe=False, status=200)    

def login(request):
    if request.method != 'POST':
        error = { "message": "only POST is allowed" }
        return JsonResponse(error, status=405)
    
    body = None
    try:
        body = json.loads(request.body)
        if len(body.keys()) != 2:
            raise Exception("invalid parameters ... expected only email and password")
        if not 'email' in body:
            raise Exception("missing email")
        if not 'password' in body:
            raise Exception("missing passord")
    except Exception as e:
        error = { "message": str(e) }
        return JsonResponse(error, status=400)

    username = body['email']
    password = body['password']

    account = get_object_or_404(models.Users, email=username, password=password)
    
    # try:
    #     newAccount = models.Users(**body)
    #     newAccount.save()
    # except IntegrityError:
    #     error = { "message": f"user {body['email']} already exits" }
    #     return JsonResponse(error, status=409)
    # except Exception as e:
    #     print(e)
    #     print(type(e))
    #     error = { "message": f"problem creating user {body['email']}" }
    #     return JsonResponse(error, status=500)
    
    # if meta.errors:
    #     print(meta.errors)
    #     data = {
    #         "message": "error"
    #     }
    #     return JsonResponse(data, safe=False, status=500)

    data = { 
       "username": account.get_username(),
       "token": account.get_session_auth_hash()
     }
    return JsonResponse(data, safe=False, status=200)

# def update_view(request, pk):
#     mymodel = get_object_or_404(MyModel, pk=pk)
#     if request.method == 'POST':
#         form = MyModelForm(request.POST, instance=mymodel)
#         if form.is_valid():
#             form.save()
#             return redirect('myapp:detail', pk=mymodel.pk)
#     else:
#         form = MyModelForm(instance=mymodel)
#     return render(request, 'myapp/update.html', {'form': form})

# def delete_view(request, pk):
#     mymodel = get_object_or_404(MyModel, pk=pk)
#     if request.method == 'POST':
#         mymodel.delete()
#         return redirect('myapp:list')  # Redirect to a list view or any other page
#     return render(request, 'myapp/delete.html', {'mymodel': mymodel})
