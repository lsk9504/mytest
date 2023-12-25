from django import forms
from .models import Freeboard
from django_summernote.widgets import SummernoteWidget

class Freeboard_Form(forms.Form):
    subject=forms.CharField(max_length=50,label="제목 ")
    content=forms.CharField(widget=SummernoteWidget(),label="내용")
    image=forms.ImageField(label="이미지 ")


"""
게시판 글 수정부분을 ModelForm이 아닌 forms.Form으로 했다.
class Freeboard_Update_Form(forms.ModelForm):
    content=forms.CharField(widget=SummernoteWidget())
    class Meta:
        model=Freeboard
        fields=['subject','content','image']   # fields='__all__' 은 모든 필드 한 번에.
"""

class Freeboard_Update_Form(forms.Form):
    subject = forms.CharField(max_length=50, label="제목 ")
    content = forms.CharField(widget=SummernoteWidget())
    image = forms.ImageField(label="이미지")


class Reply_Form(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':60}),label="하고픈 말")


