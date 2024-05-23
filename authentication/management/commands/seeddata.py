from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission
from authentication.models import User
from master.models import Province
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        if(Province.objects.count()==0):
            call_command('loaddata', 'master/seed/master_data_latest.json', verbosity=0)

        # some default generated groups
        super_group = Group.objects.create(name='Super Admin')
        admin_group = Group.objects.create(name='Admin')

        #permission to each group
        super_permissions = Permission.objects.all()
        admin_permissions = Permission.objects.all()
        
        super_group.permissions.add(*super_permissions)
        admin_group.permissions.add(*admin_permissions)

        super_user = User.objects.create_superuser(username='superadmin', password='Super@5678',email='super@admin.com')
        admin_user = User.objects.create_user(username='admin', password='Admin@1234',email='admin@admin.com')
        
        super_user.groups.add(super_group)
        admin_user.groups.add(admin_group)