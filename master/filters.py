from django_filters import rest_framework as filters
from django_filters.filters import ModelChoiceFilter
from .models import *
from .forms import *
from master.templatetags.custom_tags import has_group

CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]

form_fields = ('code', 'name_en', 'name_lc','boundary','custom_field','location',
               'display_order', 'created_at', 'updated_at', 'file_upload')


class ProvinceFilter(filters.FilterSet):

    class Meta:
        model = Province
        exclude = form_fields


class DistrictFilter(filters.FilterSet):
    province_id = ModelChoiceFilter(label='Province', queryset=Province.objects.all(),
                                    empty_label='--select province--',
                                    widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'CUSTOMJS.reloadList(this)'}))

    class Meta:
        model = District
        fields = ['province_id']


class LocalLevelFilter(filters.FilterSet):
    district_id = ModelChoiceFilter(label='District', queryset=District.objects.all(),
                                    empty_label='--select district--',
                                    widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'CUSTOMJS.reloadList(this)'}))

    class Meta:
        model = LocalLevel
        exclude = form_fields
        fields = ['district_id']


class FiscalYearFilter(filters.FilterSet):

    class Meta:
        model = FiscalYear
        exclude = form_fields


class NepaliMonthFilter(filters.FilterSet):

    class Meta:
        model = NepaliMonth
        exclude = form_fields


class GenderFilter(filters.FilterSet):
    
    class Meta:
        model = Gender
        exclude = form_fields

class CountryFilter(filters.FilterSet):
    class Meta:
        model = Country
        exclude = form_fields
        fields = []

class ActivityLogsFilter(filters.FilterSet):
    actor_id = ModelChoiceFilter(label='User', queryset=User.objects.all(),
                                    empty_label='--select user--',
                                    widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'CUSTOMJS.reloadList(this)'})) 
    
    action_type = filters.ChoiceFilter(choices=ACTION_TYPES,
                                label='Action Type',
                                empty_label='--select action type--',
                                widget=forms.Select(attrs={'class': 'form-control-sm filter-field', 'onchange': 'CUSTOMJS.reloadList(this)'}))    
    class Meta:
        model : ActivityLogs
        exclude = form_fields
        fields=['actor_id','actiob_type']