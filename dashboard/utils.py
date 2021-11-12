'''from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_registered)+text_type(user.pk)+text_type(timestamp))

token_generator=AppTokenGenerator()'''
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, room, timestamp):
        return (six.text_type(room.pk)+six.text_type(timestamp)+six.text_type(room.confirmation))


generate_token = TokenGenerator()
