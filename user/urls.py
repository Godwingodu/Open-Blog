from django.urls import path
from .views import *

urlpatterns = [

    path('userhome/',Uhome.as_view(),name="uhome"),
    path('userprofile/',UserProfiles.as_view(),name="uprofile"),    
    path('addprofile/',AddProfile.as_view(),name="addprofile"),
    path('changepassword/',ChangePassword.as_view(),name="changepassword"),
    path('updateprofile/<int:pk>',UpdateProfile.as_view(),name="updateprofile"),
    path('addblog/',AddBlogView.as_view(),name="addblog"),
    path('myblogs/',MyBlogsView.as_view(),name="myblogs"),
    path('editblogs/<int:pk>',EditBlogsView.as_view(),name="editblogs"),
    path('deleteblogs/<int:pk>',DeleteBlogsView.as_view(),name="deleteblogs"),
    path('comment/<int:bid>',Comment,name="comment"),
    path('addlike/<int:id>',AddLike,name="addlike"),
    path('removelike/<int:id>',RemoveLike,name="removelike"),
    path('follow/<int:id>',Follow,name="follow"),
    # path('searchblog/',search,name="search"),
    path('allusersprofile/<int:id>',AllUsersProfile.as_view(),name="allusersprofile"),

]
