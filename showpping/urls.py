from django.urls import path, include

from . import views

app_name = 'showpping'

urlpatterns = [
    path('mc/', views.index, name='index'),
    path('mc/<int:production_id>/', views.detail, name='detail'),
    path('mc/product_create/', views.product_create, name='product_create'),
    path('mc/product/modify/<int:product_id>/', views.product_modify, name='product_modify'),
    path('mc/product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('deny/', views.deny, name='deny'),
    path('main/', views.main, name='main'),
    path('nd/', views.review_list, name='ndlist'),
    path('nd/<int:production_id>/', views.review_detail, name='nddetail'),
    path('nd/reviewcreate/<int:production_id>/', views.review_create, name='review_create'),
    path('nd/rinfocreate/<int:production_id>/', views.rinfo_create, name='rinfo_create'),
    path('bl/', views.blind_main, name='blmain'),
    path('nd/reviewmodify/<int:review_id>/', views.review_modify, name='review_modify'),
    path('nd/reviewdelete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('nd/rinfomodify/<int:rinfo_id>/', views.rinfo_modify, name='rinfo_modify'),
    path('nd/rinfodelete/<int:rinfo_id>/', views.rinfo_delete, name='rinfo_delete'),
    path('nd/comment/create/review/<int:review_id>/', views.comment_create_review, name='comment_create_review'),
    path('nd/comment/modify/review/<int:comment_id>/', views.comment_modify_review, name='comment_modify_review'),
    path('nd/comment/delete/review/<int:comment_id>/', views.comment_delete_review, name='comment_delete_review'),
    path('nd/comment/create/rinfo/<int:rinfo_id>/', views.comment_create_rinfo, name='comment_create_rinfo'),
    path('nd/comment/modify/rinfo/<int:comment_id>/', views.comment_modify_rinfo, name='comment_modify_rinfo'),
    path('nd/comment/delete/rinfo/<int:comment_id>/', views.comment_delete_rinfo, name='comment_delete_rinfo'),
    path('nd/vote/review/<int:review_id>/', views.vote_review, name='vote_review'),
    path('product_rest_gen', views.produc_rest_gen.as_view(), name='rest_gen'),
    path('product_rest_func', views.produc_rest_func, name='rest_func'),
]