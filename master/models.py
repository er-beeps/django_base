from django.db import models
from django.contrib.gis.db import models as gis_modals
from .BaseModels import BaseModel
from django.core.validators import EmailValidator
from .validators import *


class Country(BaseModel):
    boundary = gis_modals.MultiPolygonField(null=True)
    apiid = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'mst_countries'


class Province(BaseModel):
    apiid = models.CharField(max_length=50, null=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    gps_long = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    boundary = gis_modals.MultiPolygonField(null=True)

    class Meta:
        db_table = 'mst_provinces'
        ordering = ['display_order']


class District(BaseModel):
    province_id = models.ForeignKey(Province, on_delete=models.PROTECT)
    apiid = models.CharField(max_length=50, null=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    gps_long = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    boundary = gis_modals.MultiPolygonField(null=True)

    class Meta:
        db_table = 'mst_districts'
        ordering = ['display_order']

class LocalLevel(BaseModel):
    district_id = models.ForeignKey(District, on_delete=models.PROTECT)
    apiid = models.CharField(max_length=50, null=True)
    wards_count = models.IntegerField(null=True)
    gps_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    gps_long = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    boundary = gis_modals.MultiPolygonField(null=True)

    class Meta:
        db_table = 'mst_local_levels'
        ordering = ['code']


class FiscalYear(models.Model):
    code = models.CharField(max_length=7)
    from_date_bs = models.CharField(max_length=10)
    from_date_ad = models.DateField()
    to_date_bs = models.CharField(max_length=10)
    to_date_ad = models.DateField()
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False)
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        db_table = 'mst_fiscal_years'
        ordering = ['display_order']
        
    def __str__(self):
        return "%s" %(self.code)
        
class NepaliMonth(BaseModel):
    class Meta:
        db_table = 'mst_nepali_months'
        
class Gender(BaseModel):
    class Meta:
        db_table = 'mst_genders'
        