from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.db import transaction,IntegrityError
from django.db.models import Count,Subquery,OuterRef
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from authentication.models import *
from .filters import *
from .forms import *
from .models import *
from .templatetags.custom_tags import *
from django.core.paginator import Paginator
import json,re,math,traceback,pandas as pd


global import_models
import_models = []
allowed_app_labels=['master','auth','authentication']


@login_required
def homepage(request):
    
    context = {
    
    }
    return render(request, 'layouts/dashboard.html',context)

@login_required
def redirect_to_dashboard(request):
    return redirect('/master/dashboard')


# List Operation
@login_required
def crud_list(request,slug,pid=''):
    # get model name from slug
    model = _to_pascalcase(slug)
    category = ''
     # first check for permission
    if(check_permission(request.user,('view',slug)) is False):
        return render(request,"adminlte/pages/error/403page.html")
    
    # pass page header name
    header = re.sub(r"(\w)([A-Z])", r"\1 \2", model)
    filterFields = ''

    # check if filter class is present or not
    try:
        filterClass = eval(model+'Filter')
    except NameError:
        filterClass = ''

    if filterClass:
        filterFields = filterClass(request.GET, queryset=eval(model).objects.all(),request=request)
        
    if model in import_models:
        upload_button = True
    else:
        upload_button = False
    
    tab_links= ''
    # check for tab
          
    # show filter-section only if filters are available
    hasFilter = False
    if filterFields != '' and filterFields._meta.fields:
        hasFilter = True
            
    page_num = request.GET.get('page',None)
    if page_num is not None:
        page_num = page_num
    else:
        page_num=1     
    context = {'header': header, 'slug': slug, 'hasFilter': hasFilter,'page_num':page_num,
               'filterFields': filterFields, 'upload_button': upload_button,
    }
    return render(request, "adminlte/pages/list.html", context)


# Render List Operation partial view
@login_required
def filter_crud_list(request, slug):
    modelForm = ''
    columns = ''
    labels = ''
     # first check for permission
    if(check_permission(request.user,('view',slug)) is False):
        return render(request,"adminlte/pages/error/403page.html")
    
    # check for filter class; if filter class is present return lists as queryset else return list
    hasFilterClass=False
    removeFilter= False
     ##get page num
    page_num = request.GET.get('page',None)
    
    # get model name from slug
    model = _to_pascalcase(slug)
    # buid form from model
    try:
        modelForm = eval(model+'Form')
    except NameError:
        modelForm = ''

    #allow adding elements to the table
    # get columns name and label  for list operation
    if modelForm != '':
        columns = modelForm._meta.fields
        #custom change for removing many-to-many ralation field 
        labels = modelForm._meta.labels
    # get all data from table
    lists = eval(model).objects.all()
    
    if model == 'Group':
        lists = lists.order_by('id')
    
    if request.GET is not None:
        # if filter is present
        filterClass=''
        try:
            filterClass = eval(model+'Filter')
        except NameError:
            filterClass = ''

        if filterClass != '': 
            page_param = request.GET.get('page',None)
            modified_request = request.GET.copy()
            if page_param:
                del modified_request['page']
                
            lists = filterClass(modified_request, queryset=lists)
            hasFilterClass= True
            
        try :
            exclude_lists = modelForm.exclude_on_lists() 
        except Exception as e:
            exclude_lists = ('name_lc',) 
        try :
            include_lists = modelForm.include_on_lists()
        except Exception as e:
            include_lists = '' 
    #To remove columns if they are not needed in list       
    if exclude_lists:
        original_columns = columns
        new_columns = tuple(x for x in original_columns if x not in exclude_lists)
        columns = new_columns
    
    if include_lists:
        columns= columns + include_lists
        
    #pagination
    if(filterClass):
        lists = Paginator(lists.qs,20)
    else:
        lists=Paginator(lists,20)    
    list_count = lists.count
 
    if page_num is not None:
        lists = lists.page(page_num)
    else:
        lists=lists.page(1)    
    
    context = {'columns': columns, 'labels': labels,'hasFilterClass':hasFilterClass,
               'lists': lists,'lists_count':list_count, 'slug': slug,'model':model, }
    return render(request, "adminlte/pages/partial/datatable.html", context)

# Create or Update Operation
@login_required
def crud_create_or_update(request, slug,id=0):
    model = _to_pascalcase(slug)
    header = re.sub(r"(\w)([A-Z])", r"\1 \2", model)
    if slug == 'exam_application':
        header='Research Examination Application'  
    modelForm = model+'Form'
    permissions = ''
    content_types = ''
    group_permission = ''
    user = request.user
    
    if request.method == "GET":
        if id == 0:
            # first check for permission
            if(check_permission(request.user,('add',slug)) is False):
                return render(request,"adminlte/pages/error/403page.html")
            form = eval(modelForm)(user)
            permissions = Permission.objects.filter(content_type__app_label__in=allowed_app_labels)
            content_types = ContentType.objects.filter(app_label__in=allowed_app_labels)
    
            context={
                'form':form,
                'slug':slug,
                'header':header,
                'permissions':permissions,
                'content_types':content_types,
            }
            return render(request, "adminlte/pages/create.html", context)
        else:
            # first check for permission
            if(check_permission(request.user,('change',slug)) is False):
                return render(request,"adminlte/pages/error/403page.html")
            
            entity = eval(model).objects.get(pk=id)
            
            if slug == 'user':
                form = UserEditForm(user,instance=entity)
            else:    
                form = eval(modelForm)(user,instance=entity)
               
            if slug == 'group':
                permissions = Permission.objects.filter(content_type__app_label__in=allowed_app_labels)
                content_types = ContentType.objects.filter(app_label__in=allowed_app_labels)
                
                group_permission = Group.objects.get(pk=id)
                group_permission = group_permission.permissions.filter(id__in=permissions).values_list('id')
                group_permission = [item[0] for item in group_permission]
    
            context={
                'form':form,
                'slug':slug,
                'header':header,
                'entry': entity,
                'permissions':permissions,
                'content_types':content_types,
                'permissions':permissions,
                'content_types':content_types,
                'group_permission':group_permission,
            }
            return render(request, "adminlte/pages/edit.html", context)
    else:
        message = ''
        status ='success'
        if id == 0:
            # first check for permission
            if(check_permission(request.user,('add',slug)) is False):
                return render(request,"adminlte/pages/error/403page.html")
            form = eval(modelForm)(user,request.POST, request.FILES)
        else:
            # first check for permission
            if(check_permission(request.user,('change',slug)) is False):
                return render(request,"adminlte/pages/error/403page.html")
            entity = eval(model).objects.get(pk=id)
            
            if slug == 'user':
                form = UserEditForm(user,request.POST, request.FILES, instance=entity)
            else:
                form = eval(modelForm)(user,request.POST, request.FILES, instance=entity)

        if form.is_valid():
            form.save()
            if slug == 'user':
                user_id = form.instance.id
                create_user_role(request,user_id)
                
            if slug == 'group':
                group_id = form.instance.id
                create_group_permission(request,group_id)
            
            if id == 0:
                message = 'The item has been added successfully !'
            else:
                message = 'The item has been modified successfully !'
        else:
            status = 'fail'
            message = form.errors.as_json()
        return JsonResponse({'status':status,'message': message, 'slug': slug})
    
@login_required
def crud_delete(request, slug, id):
    # first check for permission
    if(check_permission(request.user,('delete',slug)) is False):
        return render(request,"adminlte/pages/error/403page.html")
    model = _to_pascalcase(slug)
    entity = eval(model).objects.get(pk=id)
    delete_status = entity.delete()
    if(delete_status):
        status = 'success'
        value = 1
    else:
        status = 'error'
        value = 0
    return JsonResponse({'status': status, 'value': value, 'slug': slug})


def _to_pascalcase(value):
    output = ""
    first_word_passed = False
    for word in value.split("_"):
        if not word:
            output += "_"
            continue
        if first_word_passed:
            output += word.capitalize()
        else:
            output += word.capitalize()
        first_word_passed = True
    return output


# foreign key check

def check_for_foreign_key(row, slug):
    if slug == 'district':
        row['province'] = Province.objects.get(pk=row['province_id'])

    if slug == "local_level":
        row['district'] = District.objects.get(pk=row['district_id'])
        row['display_order'] = 0

    return row



## get districts
def get_districts(request,province_id):
    districts = District.objects.filter(province_id=province_id).values('id','name_en')
    districts =list(districts)
    return JsonResponse(districts,safe=False)
    
## get_local_levels
def get_local_levels(request,district_id):
    local_levels = LocalLevel.objects.filter(district_id=district_id).values('id','name_en')
    print(local_levels)
    local_levels =list(local_levels)
    return JsonResponse(local_levels,safe=False)

def get_district_locallevel(request,entry_id):
    result = Student.objects.filter(pk=entry_id).values('district_prm_id','local_level_prm_id','district_lc_id','local_level_lc_id')
    result =list(result)
    return JsonResponse(result,safe=False)


# create group permission after creating group
def create_group_permission(request,group_id):
    permissions = request.POST.getlist('permissions')
    group = Group.objects.get(pk=group_id) 
    permissions = Permission.objects.filter(id__in=permissions)
    group.permissions.set(permissions)
    return True

# create role after creating user
def create_user_role(request,user_id):
    group_id = request.POST.get('groups')
    user = User.objects.get(id=user_id)
    # check if user role already exists
    if user.groups.exists():
        user.groups.clear()
    my_group = Group.objects.filter(id=group_id).get()
    my_group.user_set.add(user)
    return True


def upload(request, slug):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            model = _to_pascalcase(slug)
            upload_file = request.FILES['file']
            return redirect('/master/'+slug+'/list')
        else:
            return JsonResponse({'status':'fail','message': 'An error occured !!', 'slug': slug})
    else:
        form = UploadFileForm()
        context = {'slug': slug}
    return render(request, 'adminlte/pages/partial/upload.html', context)
        