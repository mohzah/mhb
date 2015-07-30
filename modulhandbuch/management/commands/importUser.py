"""Define a command to import user, 
based on the relevant group"""

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils import translation
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

import getent

class Command(BaseCommand):
    """Go through all users in the group. Check whether they exist, 
    create them if not
    """

    args = ""
    help = "Go through all members of the relevant group and create if necessary"
    
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        d = dict(getent.group('mhb-app'))
        groupmembers = d['members']

        for username in groupmembers:
            user, created = User.objects.get_or_create(
                username=username
            )

            if created:
                # no local password for such users
                user.set_unusable_password()

                # allow everybody access to admin:
                user.is_staff = True

                # we do not make anybody superuser here;
                # that should happen manually

                # user.save()
                try:
                    # have to set a reasonable default group
                    g = Group.objects.get(name="lehrender")
                    user.groups.add(g)
                except:
                    print "adding user to group did not work"
                    pass

                # try to get the real-world user name :
                try:
                    d = dict(getent.passwd(username))
                    gecos = d['gecos']
                    f, l = gecos.split(' ', 1)
                    user.first_name = f
                    user.last_name = l
                except:
                    pass

                user.save()
        
            
        
        translation.deactivate()
