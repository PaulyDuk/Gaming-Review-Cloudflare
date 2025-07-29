from django.core.management.base import BaseCommand
from developer.models import Developer
from publisher.models import Publisher
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate slug fields for Developer and Publisher models.'

    def handle(self, *args, **options):
        dev_count = 0
        pub_count = 0
        for dev in Developer.objects.all():
            if not dev.slug:
                dev.slug = slugify(dev.name)
                dev.save()
                dev_count += 1
        for pub in Publisher.objects.all():
            if not pub.slug:
                pub.slug = slugify(pub.name)
                pub.save()
                pub_count += 1
        self.stdout.write(self.style.SUCCESS(f'Populated {dev_count} developer slugs and {pub_count} publisher slugs.'))
