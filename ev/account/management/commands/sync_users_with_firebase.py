from django.core.management.base import BaseCommand, CommandError
from account.models import Account
from ev.auth import create_user_firebase
from django.conf import settings


class Command(BaseCommand):
    help = 'Sync users with firebase ...'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user_id', required=False)

    def handle(self, *args, **options):
        if options["user_id"] is None:
            # sync all unsynced users
            users = Account.objects.filter(firebase_uid=None)
            for user in users:
                print("email ", user.email)
                firebase_user = create_user_firebase(
                    user.email, settings.SECRET_KEY)
                # set firebase_user.uid as new password for users
                user.set_password(firebase_user.uid)
                user.is_password_changed = False
                user.firebase_uid = firebase_user.uid
                user.save()
