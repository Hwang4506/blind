from django import forms
from showpping.models import Product_info, Review, Rinfo, Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product_info  # 사용할 모델
        fields = ['First_Class', 'Second_Class', 'Product_Name', 'Price',
                  'Expiration_Date', 'Basic_Information', 'Notice', 'Additional_Information']
        widgets = {
            'Basic_Information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Notice': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Additional_Information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'First_Class' : '대분류',
            'Second_Class' : '중분류',
            'Product_Name' : '제품명',
            'Price' : '가격',
            'Expiration_Date' : '유통기한',
            'Basic_Information' : '기본정보',
            'Notice' : '유의사항',
            'Additional_Information' : '추가정보',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['User_Review']
        labels = {
            'User_Review': '리뷰 내용',
        }

class RinfoForm(forms.ModelForm):
    class Meta:
        model = Rinfo
        fields = ['Realtime_Information']
        labels = {
            'Realtime_Information': '실시간정보 내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }