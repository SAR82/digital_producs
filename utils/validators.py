from django.core.exceptions import ValidationError
import re
from datetime import date


def validate_iranian_mobile(value):
    if not re.match(r'^989[0-3,9]\d{8}$', str(value)):
        raise ValidationError('شماره موبایل وارد شده معتبر نیست. باید با 989 شروع شده و 11 رقم باشد.')


def validate_username(value):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{3,31}$', value):
        raise ValidationError('نام کاربری باید با حرف شروع شده و شامل 4 تا 32 حرف، عدد یا آندرلاین باشد.')


def validate_strong_password(value):
    if len(value) < 8:
        raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('رمز عبور باید حداقل یک عدد داشته باشد.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('رمز عبور باید حداقل یک کاراکتر خاص داشته باشد.')



def validate_birthdate(value):
    if value > date.today():
        raise ValidationError('تاریخ تولد نمی‌تواند در آینده باشد.')


def validate_persian_only(value):
    if not re.match(r'^[آ-ی\s]+$', value):
        raise ValidationError('این فیلد فقط باید شامل حروف فارسی باشد.')


def validate_sku(value):
    if not re.match(r'^[A-Z][A-Z0-9\-]{4,19}$', value):
        raise ValidationError(
            'SKU باید با حرف بزرگ شروع شود و فقط شامل حروف بزرگ، عدد و خط تیره باشد (۵ تا ۲۰ کاراکتر).'
        )