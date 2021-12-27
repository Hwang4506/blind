from django.shortcuts import render, get_object_or_404, redirect
from .models import Product_info, Review, Blind_User, Rinfo, Comment
from .forms import ProductForm, ReviewForm, RinfoForm, CommentForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from .serializers import ProductinfoSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

@login_required(login_url='common:login')
@permission_required('showpping.view_product_info', login_url='showpping:deny', raise_exception=False)
def index(request):
    """
    제조사/유통사/매장 제품 정보 목록 출력
    """
    production_list = Product_info.objects.order_by('-Expiration_Date')
    context = {'production_list': production_list}
    return render(request, 'showpping/production_list.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_product_info', login_url='showpping:deny', raise_exception=False)
def detail(request, production_id):
    """
    제조사/유통사/매장 제품 정보 내용 출력
    """
    production = get_object_or_404(Product_info, pk=production_id)
    review = request.GET.get(Review)
    rinfo = request.GET.get(Rinfo)
    context = {'production': production, 'review': review, 'rinfo': rinfo}
    return render(request, 'showpping/production_detail.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_product_info', login_url='showpping:deny', raise_exception=False)
def product_create(request):
    """
      제조사/유통사/매장 제품 등록
      """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('showpping:index')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'showpping/product_form.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_product_info', login_url='showpping:deny', raise_exception=False)
def product_modify(request, product_id):
    """
    제조사/유통사/매장 제품정보 수정
    """
    product = get_object_or_404(Product_info, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('showpping:detail', production_id=product.id)
    else:
        form = ProductForm(instance=product)
    context = {'form': form}
    return render(request, 'showpping/product_form.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_product_info', login_url='showpping:deny', raise_exception=False)
def product_delete(request, product_id):
    """
    제조사/유통사/매장 제품정보 삭제
    """
    product = get_object_or_404(Product_info, pk=product_id)
    product.delete()
    return redirect('showpping:index')

def deny(request):
    """
        권한없음
                   """
    return render(request, 'showpping/deny.html')

def main(request):
    """
        메인 페이지 : 유저 선택
           """
    return render(request, 'showpping/main.html')

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def review_list(request):
    """
    비장애인 제품 목록 출력
    """
    production_list = Product_info.objects.order_by('-Expiration_Date')
    context = {'production_list': production_list}
    return render(request, 'showpping/review_list.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def review_detail(request, production_id):
    """
    비장애인 제품 정보 내용 출력
    """
    production = get_object_or_404(Product_info, pk=production_id)
    review = request.GET.get(Review)
    rinfo = request.GET.get(Rinfo)
    context = {'production': production, 'review': review, 'rinfo': rinfo}
    return render(request, 'showpping/review_detail.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def review_create(request, production_id):
    """
    리뷰 등록
    """
    production = get_object_or_404(Product_info, pk=production_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.Author = request.user  # author 속성에 로그인 계정 저장
            review.create_date = timezone.now()
            review.Product = production
            review.save()
            return redirect('showpping:nddetail', production_id=production.id)
    else:
        form = ReviewForm()
    context = {'production': production, 'form': form}
    return render(request, 'showpping/review_detail.html', context)


@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def rinfo_create(request, production_id):
    """
    실시간정보 등록
    """
    production = get_object_or_404(Product_info, pk=production_id)
    if request.method == "POST":
        form2 = RinfoForm(request.POST)
        if form2.is_valid():
            rinfo = form2.save(commit=False)
            rinfo.Author = request.user  # author 속성에 로그인 계정 저장
            rinfo.create_date = timezone.now()
            rinfo.Product = production
            rinfo.save()
            return redirect('showpping:nddetail', production_id=production.id)
    else:
        form2 = RinfoForm()
    context = {'production': production, 'form2': form2}
    return render(request, 'showpping/review_detail.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def review_modify(request, review_id):
    """
    리뷰 수정
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.Author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('showpping:nddetail', production_id=review.Product.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.modify_date = timezone.now()
            review.save()
            return redirect('showpping:nddetail', production_id=review.Product.id)
    else:
        form = ReviewForm(instance=review)
    context = {'review': review, 'form': form}
    return render(request, 'showpping/review_form.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def review_delete(request, review_id):
    """
    리뷰 삭제
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.Author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        review.delete()
    return redirect('showpping:nddetail', production_id=review.Product.id)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def rinfo_modify(request, rinfo_id):
    """
    실시간정보 수정
    """
    rinfo = get_object_or_404(Rinfo, pk=rinfo_id)
    if request.user != rinfo.Author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('showpping:nddetail', production_id=rinfo.Product.id)

    if request.method == "POST":
        form = RinfoForm(request.POST, instance=rinfo)
        if form.is_valid():
            rinfo = form.save(commit=False)
            rinfo.modify_date = timezone.now()
            rinfo.save()
            return redirect('showpping:nddetail', production_id=rinfo.Product.id)
    else:
        form = RinfoForm(instance=rinfo)
    context = {'rinfo': rinfo, 'form': form}
    return render(request, 'showpping/rinfo_form.html', context)

@login_required(login_url='common:login')
@permission_required('showpping.view_review', login_url='showpping:deny', raise_exception=False)
def rinfo_delete(request, rinfo_id):
    """
    실시간정보 삭제
    """
    rinfo = get_object_or_404(Rinfo, pk=rinfo_id)
    if request.user != rinfo.Author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        rinfo.delete()
    return redirect('showpping:nddetail', production_id=rinfo.Product.id)

@login_required(login_url='common:login')
def comment_create_review(request, review_id):
    """
    리뷰 댓글등록
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.review = review
            comment.save()
            return redirect('showpping:nddetail', production_id=comment.review.Product.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'showpping/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_review(request, comment_id):
    """
    리뷰 댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('showpping:nddetail', production_id=comment.review.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('showpping:nddetail', production_id=comment.review.Product.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'showpping/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_review(request, comment_id):
    """
    리뷰 댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('showpping:nddetail', production_id=comment.review.Product.id)
    else:
        comment.delete()
    return redirect('showpping:nddetail', production_id=comment.review.Product.id)

@login_required(login_url='common:login')
def comment_create_rinfo(request, rinfo_id):
    """
    실시간정보 댓글등록
    """
    rinfo = get_object_or_404(Rinfo, pk=rinfo_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.rinfo = rinfo
            comment.save()
            return redirect('showpping:nddetail', production_id=comment.rinfo.Product.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'showpping/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_rinfo(request, comment_id):
    """
    실시간정보 댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('showpping:nddetail', production_id=comment.rinfo.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('showpping:nddetail', production_id=comment.rinfo.Product.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'showpping/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_rinfo(request, comment_id):
    """
    실시간정보 댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('showpping:nddetail', production_id=comment.rinfo.Product.id)
    else:
        comment.delete()
    return redirect('showpping:nddetail', production_id=comment.rinfo.Product.id)

@login_required(login_url='common:login')
def vote_review(request, review_id):
    """
    리뷰 추천등록
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.Author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        review.voter.add(request.user)
    return redirect('showpping:nddetail', production_id=review.Product.id)

@login_required(login_url='common:login')
@permission_required('showpping.view_blind_user', login_url='showpping:deny', raise_exception=False)
def blind_main(request):
    """
        장애인유저 메인화면
                        """
    return render(request, 'showpping/blmain.html')

class produc_rest_gen(generics.ListCreateAPIView):
    queryset = Product_info.objects.all()
    serializer_class = ProductinfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('First_Class', 'Second_Class', 'Product_Name', 'Manufacturer', 'Price',
                    'Expiration_Date', 'Basic_Information',
                    'Notice', 'Additional_Information', 'barcode_number'
                    )

@csrf_exempt
def produc_rest_func(request):
    if request.method == 'GET':
        query_set = Product_info.objects.all()
        serializer = ProductinfoSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductinfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()       # DB저장
            # sendPushp(serializer.data)
            # print("비데이터의 형식 : ", type(serializer.data))
            # print("비데이터 : ", serializer.data)
            # print("아이디 : ", serializer.data["id"])
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)