import utils

from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand


STATICFILES_VENDOR_DIR = getattr(settings,'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES = {
    "gsap.min.js": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.0/gsap.min.js",
    "gsap.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.0/gsap.min.js.map",
    "ScrollTrigger.min.js": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.0/ScrollTrigger.min.js",
    "ScrollTrigger.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.0/ScrollTrigger.min.js.map",


    "typed.min.js": "https://cdnjs.cloudflare.com/ajax/libs/typed.js/2.0.10/typed.min.js",
    "typed.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/typed.js/2.0.10/typed.min.js.map",

    "bootstrap-icons.min.css": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "fonts/bootstrap-icons.woff": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff",
    "fonts/bootstrap-icons.woff2": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2",
    "material-icons.css" : "https://fonts.googleapis.com/icon?family=Material+Icons",
    
    "htmx.min.js": "https://unpkg.com/htmx.org@2.0.4",
}

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading vendor static files")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = utils.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download {url}')
                )
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS('Successfully updated all vendor static files.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Some files were not updated.')
            )

