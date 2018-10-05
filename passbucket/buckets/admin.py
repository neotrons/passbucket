from django.contrib import admin
from .models import Bucket
from .forms import BucketForm
# Register your models here.


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    form = BucketForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(BucketAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form
