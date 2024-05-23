from django.db import models


class BaseModel(models.Model):
    code = models.IntegerField()
    name_en = models.CharField(max_length=100)
    name_lc = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False)
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ['display_order']

    def __str__(self):
        return self.name_en