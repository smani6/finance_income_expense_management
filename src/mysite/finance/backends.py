from django.contrib.auth.models import User
from models import CustomUser, Account
import traceback
from django.contrib.auth.hashers import (make_password,)
import time
import re
from django.contrib.auth.hashers import SHA1PasswordHasher
import logging
log = logging.getLogger(__name__)


class MyCustomBackend:

    def authenticate(self, username=None, password=None):
        log.debug("Inside Method MyCustomBackend::authenticate")
        log.debug("Request username - {0} and password {1}".format(username, password))
        account_id = None
        try:
            pattern = "^[A-Za-z0-9._+\-\']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
            if re.match(pattern, username):
                user = 'email'
                log.debug('Entered username is email field')
            else:
                user = 'mobile'
                log.debug('Entered username is mobile field')

            if user == 'email':
                account_obj = Account.objects.get(email=username)
                log.debug('Account id for the given email - {0}'.format(account_obj.account_id))
            else:
                account_obj = Account.objects.get(phone_number=username)
                log.debug('Account id for the given mobile - {0}'.format(account_obj.account_id))

            try:
                if str(password) == str(account_obj.password):
                    log.debug('Password match - so setting password_flag to True')
                    password_flag = True
                else:
                    log.debug('Password dont match - so setting password_flag to False')
                    password_flag = False

            except Exception as e:
                log.error(e)
                return None

            if password_flag:
                account_id = account_obj.account_id
                log.debug(
                    'Password flag set and assigning account_id from account_obj - {0}'.format(account_id))
            else:
                log.debug('Password flag not set. Hence raising Exception')
                raise Exception

        except Exception as e:
            log.error(e)
            log.error("Exception raised - so returning None")
            return None

        try:
            log.debug("Check if the user exists in Django's local database")
            user = User.objects.get(email=username)
            log.debug("User exists in django's auth table - updating account_id to it")
            CustomUser.objects.filter(user_id=user.id).update(Account_id=account_id)
        except User.DoesNotExist:
            log.warning("User DoesNotExists Create a user in Django's local database")
            user = User.objects.create_user(time.time(), email=username)
            CustomUser.objects.create(user_id=user.id, Account_id=account_id)
            log.debug("User created and Returning User")
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
