from django import forms
from .models import Item,Company,Maincategory,Subcategory


class Input_form(forms.Form):

    item = forms.ModelChoiceField(
        label='제품명',
        queryset = Item.objects.only('name').order_by('name'),  #Item 테이블의 name 필드 값들만 가져옵니다.
        #initial = 0    #initial=0은 default 값으로 첫번째 리스트 값을 쓰겠다는 뜻
        )

    company = forms.ModelChoiceField(
        label='회사명',
        queryset=Company.objects.filter(inout='in').only('name').order_by('name'),
        #initial = 0
    )

    ITEM_QUANTITY = [(i, str(i)) for i in range(1, 11)] #ChoiceField는 펼쳐지는 가지수에 제한이 있지만, TypedChoiceField는 람다식 가능
    quantity =forms.TypedChoiceField(label='수량',choices=ITEM_QUANTITY,coerce=int) #앞에 i가 저장되고, 뒤에 i는 문자열로 만들어서 눈에 보이게 한다.
    # coerce는 TypedChoiceField의 필수 요소로 저장되는 데이터 타입을 정의.


class Output_form(forms.Form):
    item=forms.ModelChoiceField(
        label='제품명',
        queryset=Item.objects.only('name').order_by('name'),
    )

    company=forms.ModelChoiceField(
        label='회사명',
        queryset=Company.objects.filter(inout='out').only('name').order_by('name'),
    )

    ITEM_QUANTITY=[(i,str(i)) for i in range(1,11)]
    quantity=forms.TypedChoiceField(label='수량',choices=ITEM_QUANTITY,coerce=int)

"""
class Erp_form(forms.Form):

    main_category=forms.ModelChoiceField(
        queryset=Maincategory.objects.only('name').order_by('name'),
        initial=0,
        widget=forms.Select(attrs={'onchange': "go(this.value);"})
    )

    sub_category=forms.ModelChoiceField(
        queryset=Subcategory.objects.only('name').order_by('name'),
        initial=0,
        widget=forms.Select(attrs={'onchange': "go(this.value);"})
    )
"""

class Erp_form(forms.Form):
    main_category=forms.ModelChoiceField(queryset=Maincategory.objects.all(),
    widget=forms.Select(attrs={"hx-get": "load_subs/" , "hx-target": "#id_sub_category","style":"width:100px"}))
    sub_category=forms.ModelChoiceField(queryset=Subcategory.objects.none(),widget=forms.Select(attrs={"hx-get": "load_items/", "hx-target": "#id_item",'style': 'width:100px'}))
    item=forms.ModelChoiceField(queryset=Item.objects.none(),widget=forms.Select(attrs={'style':'width:200px'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "main_category" in self.data:   # form=Erp_form(request.POST) 시 넘어온 값들은 self.data에 딕셔너리 형태로 존재한다.
            print(self.data)  # <QueryDict: {'csrfmiddlewaretoken': ['Dp1qxd2CPwui2JYJvLuXjLGXFbQqJNJ6ggiprOytSvX8Q6qVWxfGiGJv3WRMbIBz'], 'main_category': ['6'], 'sub_category': ['13'], 'item': ['22']}>
            main_category_id = int(self.data.get("main_category"))
            self.fields["sub_category"].queryset = Subcategory.objects.filter(category_id=main_category_id)
            print(self.fields["sub_category"].queryset) #<QuerySet [<Subcategory: Table>, <Subcategory: Tent>, <Subcategory: Kitchen>, <Subcategory: Chair>]>

        if "item" in self.data:
            sub_category_id=int(self.data.get("sub_category"))
            self.fields['item'].queryset=Item.objects.filter(item_category_id=sub_category_id)
            print(self.fields['item'].queryset) #<QuerySet [<Item: tent green>, <Item: tent bushnell>, <Item: tent colmen>]>


