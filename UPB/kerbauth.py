from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

import kerberos
import getent
import re


class KerbAuth(ModelBackend):

    def __init__(self):
        self.group_name = "lehrender"
        group, created = Group.objects.get_or_create(name=self.group_name)
        if created:
            permissions = Permission.objects.all()
            for p in permissions:
                if 'modulhandbuch' in str(p):
                    group.permissions.add(p)
        super(KerbAuth, self).__init__()

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        # print "trying to authenticate ", username, password

        try:
            kerberos.checkPassword(username, password,
                                   "",  settings.KRB5_REALM)
        except kerberos.BasicAuthError:
            # print "Kerberos auth failed"
            return None

        # print "kerberos succeeded"

        with open('/etc/apache2/htgroup') as f:
            text = f.read()
            pattern = '^modulhandbuch-mb:.*$'
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                if not username + '@UNI-PADERBORN.DE' in match.group(0):
                    return None
        # TODO: think how to better integrate this with the
        # django permission system. depending on group
        # membership, assign different permissions.
        # this requires a better understanding of the
        # way django permissions are expressed :-(
        if False and settings.RUN_ON_WEBAPP:
            webappgroup = dict(getent.group('mhb-app'))
            if username not in webappgroup['members']:
                return None

        user, created = User.objects.get_or_create(
            username=username
        )

        # print "user, created: ", user, type(user), created

        if created:
            # no local password for such users
            user.set_unusable_password()

            # allow everybody access to admin:
            user.is_staff = True

            # we do not make anybody superuser here;
            # that should happen manually

            try:
                # have to set a reasonable default group
                g = Group.objects.get(name=self.group_name)
                user.groups.add(g)
            except:
                # print "adding user to group did not work"
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

        return user

    # def get_user(self, user_id):
    #     print "getting user: ", user_id

    #     UserModel = get_user_model()
    #     try:
    #         user = UserModel._default_manager.get(pk=user_id)
    #         print "user: ", user
    #     except UserModel.DoesNotExist:
    #         return None

    #     return user
