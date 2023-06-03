import shortuuid
import qrcode
from qrcode.image.svg import SvgImage
from django.http import JsonResponse
from io import BytesIO, StringIO
from django.contrib import auth
import random
from django.conf import settings

  

def code_generator():
    code = shortuuid
    ref_id = code.ShortUUID().random(length = 10)
    return ref_id

def _transaction_id_generator():
    code = shortuuid
    tr_id = code.ShortUUID().random(length = 12)
    return tr_id

def token_generator():
    token=[random.randint(1, 9) for _ in range(6)]
    return token
    




def decode_qrcode(e):
    f = StringIO()
    e.print_ascii(out=f)
    f.seek(0)
    outPut = f.read()
    return outPut


def login_ajax(request):
    if request.is_ajax:
        email = request.POST['user_email']
        password = request.POST['user_password']

        object = auth.authenticate(email=email.lower(), password=password)
        if object is not None:
            auth.login(request, object)
            next_url = settings.LOGIN_REDIRECT_URL

            return JsonResponse(next_url, safe=False)
        else:
            return JsonResponse('Error', safe=False)





