# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from demo.models import Post, LikeHistory,ImageUpload
from django.contrib.auth.models import User as AuthUser

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status, viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


import json



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
 
    reply = {}
    try:

        user = AuthUser.objects.filter(username = request.data['username']).first()
        if user:
            
            reply['status'] = "DUPLICATE ENTRY"
            reply['error_code'] = "INVALID_" 
                            
        else:
            user = AuthUser()
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')
            user.password = request.POST.get('password')
            user.save()

            user.set_password(request.data['password'])
            user.save()

    except Exception as e:
        print(str(e))
        reply['status'] = "ERROR"
        reply['message'] = "Server: User not created. Please contact support or retry."
        reply['error_code'] = "DB_CREATE_FAILED"
        dict_obj = json.dumps(reply)
        return HttpResponse(json.dumps(reply), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    reply['status'] = "SUCCESS"
    reply['message'] = "Signup was sucessful"
    dict_obj = json.dumps(reply)
    return HttpResponse(dict_obj, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request): 
    reply = {}
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    try:
       
        if uname != None and pwd != None:
            user = authenticate(username = uname, password = pwd)
            if user is not None:
                return HttpResponse('Login Success', status =  status.HTTP_202_ACCEPTED)
            else:
                return HttpResponse('Invalid Login Credentials',  status = status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse('Invaid Login Details')

    except Exception as ex:
        reply['status'] = "ERROR"
        reply['message'] = str(ex)
        print(str(ex))
     
        return HttpResponse( status = status.HTTP_400_BAD_REQUEST)



class PostViewSet(viewsets.GenericViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self,request):

        if request.user.is_superuser:
            
            post = Post()
            post.description = request.POST.get('description')
            post.user = request.user
            post.save()

            for img in request.FILES.getlist('img'):
                ph = ImageUpload(image = img, post=post)
                ph.save()
        

            return HttpResponse ("**....POST UPLOADED SUCESSFULLY....**", status = status.HTTP_202_ACCEPTED)

        else:
            return HttpResponse (" NOT AUTHORIZED", status = status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        post = Post.objects.all()
        likedict = []
       
        for p in post:
            reply = {}
            li = 0
            dl = 0
            like = LikeHistory.objects.filter(post = p)
           
            for lk in like:
                if lk.like:
                    li = li + 1
                
                if lk.dislike:
                    dl = dl + 1
            lk = LikeHistory.objects.filter(post = p, user= request.user).first()
            
            
            reply["Post"] = str(p.id)
            reply["Likes"] = str(li)
            reply["Dislikes"] = str(dl)
            if lk is not None:
                reply["Liked"] = str(lk.like)
                reply["Disliked"] = str(lk.dislike)
            reply["Created Date"] = str(p.postedDate)

            imglist = ImageUpload.objects.filter(post= p)
            imgdict = []
            for img in imglist:
                imgdict.append(img.image)
            reply["Image"] = str(imgdict)

            likedict.append(reply)

        return HttpResponse(json.dumps(likedict), status = status.HTTP_200_OK)





class LikeViewSet(viewsets.GenericViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self,request):

        post = Post.objects.filter(id = request.data['post']).first()
        if post is not None:
            likehistory = LikeHistory.objects.filter(user = request.user, post = post).first()
            
            if likehistory is not None:
                if 'like' in request.data:
                    likehistory.like = request.data ['like']
                    likehistory.dislike = False
                    likehistory.save()

                if 'dislike' in request.data:
                    likehistory.dislike = request.data['dislike']
                    likehistory.like = False
                    likehistory.save()

            else:
                
                like = LikeHistory()
                like.user = request.user
                
                if 'like' in request.data:
                    like.like = request.data ['like']
                
                if 'dislike' in request.data:
                    like.dislike = request.data['dislike']

                like.post = post
                like.save()

            return HttpResponse (" SUCESSFULL", status = status.HTTP_202_ACCEPTED)

        else:
            return HttpResponse (" NOT FOUND", status = status.HTTP_404_NOT_FOUND)

                

    def list(self, request):
        post = Post.objects.all()
        likedict = []
       
        for p in post:
            reply = {}
            li = 0
            dl = 0
            like = LikeHistory.objects.filter(post = p)
           
            for lk in like:
                if lk.like:
                    li = li + 1
                
                if lk.dislike:
                    dl = dl + 1
            reply["Post"] = str(p.id)
            reply["Likes"] = str(li)
            reply["Dislikes"] = str(dl)
            likedict.append(reply)
        return HttpResponse(json.dumps(likedict), status = status.HTTP_200_OK)
