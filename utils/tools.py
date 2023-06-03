import qrcode
from qrcode.image.svg import SvgImage
from django.http import JsonResponse
from io import BytesIO, StringIO


def qr_code_generator(e):
    stream = BytesIO()
    
    _converted = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
    )
    _converted.add_data(e)
    _converted.make(fit=True)
    qrCodeDone = _converted.make_image(
        image_factory=SvgImage
        )

    type(qrCodeDone)
    qrCodeDone.save(stream)
    return stream.getvalue().decode()