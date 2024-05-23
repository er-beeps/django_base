from django import forms
from .models import *
from authentication.models import ActivityLogs
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField


def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')


global form_labels, form_fields
form_labels = {
    'code': 'Code',
    'name_en': 'Name',
    'name_lc': 'नाम',
    'display_order': 'Display Order',
    'is_active' :'Active Status'
}

form_fields = ('code','name_en', 'name_lc', 'display_order','is_active')


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget.html"
    
    
class UploadFileForm(forms.Form):
    file = forms.FileField()

class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-3' 

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(ProvinceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-3' 

        if Province.objects.all().count() > 0:
            self.fields['code'].widget.attrs['value'] = Province.objects.order_by(
                '-code')[0].code+1
            self.fields['display_order'].widget.attrs['value'] = Province.objects.order_by(
                '-display_order')[0].display_order+1


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('code','province_id','name_en', 'name_lc', 'display_order','is_active')
        labels = {
                'code': 'Code',
                'province_id': 'Province',
                'name_en': 'Name',
                'name_lc': 'नाम',
                'display_order': 'Display Order',
                'is_active' :'Active Status'
            }

    def __init__(self, user=None, *args, **kwargs):
        super(DistrictForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-3' 
        
        if District.objects.all().count() > 0:
            self.fields['code'].widget.attrs['value'] = District.objects.order_by(
                '-code')[0].code+1
            self.fields['display_order'].widget.attrs['value'] = District.objects.order_by(
                '-display_order')[0].display_order+1

class LocalLevelForm(forms.ModelForm):
    class Meta:
        model = LocalLevel
        fields = ('code','district_id','name_en', 'name_lc','wards_count','gps_lat','gps_long', 'display_order','is_active')
        
        form_labels.update({})
        labels = {
                    'code': 'Code',
                    'name_en': 'Name',
                    'name_lc': 'नाम',
                    'district_id': 'District',
                    'wards_count': 'Wards Count',
                    'gps_lat': 'GPS Latitude',
                    'gps_long': 'GPS Longitude',
                    'display_order': 'Display Order',
                    'is_active' :'Active Status'
                }

    def __init__(self, user=None, *args, **kwargs):
        super(LocalLevelForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            if(visible.name in ['name_en','name_lc','gps_lat','gps_long','district_id']):
                visible.field.widget.attrs['col'] = 'col-md-3'
            else:
                visible.field.widget.attrs['col']='col-md-3'   
                    
        if LocalLevel.objects.all().count() > 0:
            self.fields['code'].widget.attrs['value'] = LocalLevel.objects.order_by(
                '-code')[0].code+1
            self.fields['display_order'].widget.attrs['value'] = LocalLevel.objects.order_by(
                '-display_order')[0].display_order+1


class FiscalYearForm(forms.ModelForm):
    class Meta:
        model = FiscalYear
        fields = ('code', 'from_date_bs', 'from_date_ad','to_date_bs', 'to_date_ad', 'display_order','is_active')
        labels = {
                    'code': 'Code',
                    'from_date_bs': 'From Date(B.S)',
                    'from_date_ad': 'From Date(A.D)',
                    'to_date_bs': 'To Date(B.S)',
                    'to_date_ad': 'To Date(A.D)',
                    'display_order': 'Display Order',
                    'is_active' :'Active Status'
                }
        widgets = {
            'from_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'from_date_bs', 'relatedId': 'from_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'to_date_bs': forms.TextInput(attrs={'class': 'input-nepali-date', 'id': 'to_date_bs', 'relatedId': 'to_date_ad', 'placeholder': 'yyyy-mm-dd', 'onclick': 'fieldDateChange(this)'}),
            'from_date_ad': forms.DateInput(attrs={'id': 'from_date_ad', 'type': 'date'}),
            'to_date_ad': forms.DateInput(attrs={'id': 'to_date_ad', 'type': 'date'})
        }
        
    def __init__(self, user=None, *args, **kwargs):
        super(FiscalYearForm, self).__init__(*args, **kwargs)
        self.fields['display_order'].widget.attrs['value'] = 1
 
        for visible in self.visible_fields():
            if(visible.name in ['from_date_bs','from_date_ad','to_date_bs','to_date_ad','code','display_order']):
                visible.field.widget.attrs['col'] = 'col-md-2'
        if FiscalYear.objects.all().count() > 0:
            self.fields['display_order'].widget.attrs['value'] = FiscalYear.objects.order_by(
                '-display_order')[0].display_order+1
                    


class NepaliMonthForm(forms.ModelForm):
    class Meta:
        model = NepaliMonth
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(NepaliMonthForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-3'
            
        if NepaliMonth.objects.all().count() > 0:
            self.fields['code'].widget.attrs['value'] = NepaliMonth.objects.order_by(
                '-code')[0].code+1
            self.fields['display_order'].widget.attrs['value'] = NepaliMonth.objects.order_by(
                '-display_order')[0].display_order+1


class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = form_fields
        labels = form_labels

    def __init__(self, user=None, *args, **kwargs):
        super(GenderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-3'

        if Gender.objects.all().count() > 0:
            self.fields['code'].widget.attrs['value'] = Gender.objects.order_by(
                '-code')[0].code+1
            self.fields['display_order'].widget.attrs['value'] = Gender.objects.order_by(
                '-display_order')[0].display_order+1
            
class SelectSingleWidget(forms.widgets.SelectMultiple):
    allow_multiple_selected = False
    help_text=''
        
class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','groups')
        labels = {
            'first_name':'First Name',
            'last_name':'Last Name',
            'username':'User Name',
            'email':'Email address',
            'groups':'Role',
            
        }
        help_texts = {
            'username': None,
            'groups': None,
        }
        widgets = {
            'groups': SelectSingleWidget(attrs={'id':'group_id','required':'true'}),
        }
        
    def exclude_on_lists():
        return ('program','batch')  
        
    def __init__(self,user=None,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
                visible.field.widget.attrs['col'] = 'col-md-4'
        # Order groups by id
        if user.groups.first().id == 1:
            self.fields['groups'].queryset = Group.objects.all().order_by('id')
        else:    
            self.fields['groups'].queryset = Group.objects.exclude(id=1).order_by('id')
        
class UserEditForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        help_text = ''
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','groups',)
        labels = {
            'first_name':'First Name',
            'last_name':'Last Name',
            'username':'User Name',
            'email':'Email address',
          
        }
        help_texts = {
            'username': None,
            'groups': None,
        }
        widgets = {
            'groups': SelectSingleWidget(attrs={'id':'group_id','required':'true'}),
        }

    def __init__(self,user=None,*args,**kwargs):
        super(UserEditForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
                visible.field.widget.attrs['col'] = 'col-md-4'
                
        # Order groups by id
        if user.groups.first().id == 1:
            self.fields['groups'].queryset = Group.objects.all().order_by('id')
        else:    
            self.fields['groups'].queryset = Group.objects.exclude(id=1).order_by('id')
    
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name':'Role Name',
        }
    def __init__(self, user=None, *args, **kwargs):
        super(GroupForm,self).__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['col'] = 'col-md-12' 
            
class ActivityLogsForm(forms.ModelForm):
    class Meta:
        model = ActivityLogs
        fields = ('actor', 'request_url','request_method','model','action_type','status','response_code','ip_address','datetime','extra_data')
        labels = {
               'actor':'User',
               'request_url':'Request URL',
               'request_method':'Request Method',
               'response_code':'Response Code',
               'datetime':'Date Time',
               'extra_data':'Extra Data',
               'ip_address':'IP Address',
               'action_type':'Action Type',
               'status':'Status',
               'model':'Model',
            }

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityLogsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['readonly'] = True
            if visible.name in ['extra_data']:
                visible.field.widget.attrs['col'] = 'col-md-12'
            elif visible.name in ['request_url']:
                visible.field.widget.attrs['col'] = 'col-md-8'
            elif visible.name in ['status','response_code','datetime','ip_address']:
                visible.field.widget.attrs['col'] = 'col-md-3'
            else:
                visible.field.widget.attrs['col'] = 'col-md-4'
