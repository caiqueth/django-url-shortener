import random
import string

import qrcode

from urlshortener.models import UrlRegister


def url_generator(original_url: str, url_root: str) -> UrlRegister:

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    existing = UrlRegister.objects.filter(original_url=original_url)

    if not existing:
        new_id = generate_new_id()
        url = url_root + "/" + new_id

        qr_code_path = f"qrcodes/{new_id}.png"
        qr_code = qrcode.make(url)
        qr_code.save("media/" + qr_code_path)

        u = UrlRegister(
            original_url=original_url,
            new_url=url,
            qr_code=qr_code_path
        )

        u.save()

    else:
        u = existing[0]

    return u

def generate_new_id() -> str:

    while True:
        _new_url = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=12))
        existing = UrlRegister.objects.filter(new_url=_new_url)
        if not existing:
            return _new_url
