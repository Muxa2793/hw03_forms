from django.core.management.base import BaseCommand

from posts.models import Group
from posts.parsers.xlsx_group_parser import XLSXGroupParser


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        file = options['file']
        groups = XLSXGroupParser(file[0])
        for group in groups:
            Group.objects.get_or_create(
                title=group.title,
                slug=group.slug,
                description=group.description
            )
        self.stdout.write(self.style.SUCCESS('Command complete'))
