from django.db.utils import DatabaseError
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.migrations.recorder import MigrationRecorder
from dektools.zip import compress_files, decompress_files
from dekdjtools.utils.migration import list_migrations, project_dir
from dekdjselfmigration.models import MigrationRecord

try:
    from psycopg2.errors import DatabaseError as PsqlDatabaseError
except ModuleNotFoundError:
    class PsqlDatabaseError(Exception):
        pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='[.args]', nargs='*', help='args',
        )

    def handle(self, *args, **options):
        mid = args[0]
        try:
            exists = MigrationRecorder.Migration.objects.filter(app=__name__.partition('.')[0]).exists()
        except (DatabaseError, PsqlDatabaseError):
            exists = False
        if not exists:
            call_command('makemigrations')
            call_command('migrate')
        if MigrationRecord.objects.filter(mid=mid).exists():
            call_command('makemigrations')
            return
        queryset = MigrationRecord.objects.order_by('-id')
        try:
            mr = queryset.first()
        except DatabaseError:
            mr = None
        if mr:
            call_command('ddtdelmigrations')
            fp_set = decompress_files(mr.content, project_dir, True)
        else:
            fp_set = set()
        call_command('makemigrations')
        root_dir, filepath_set = list_migrations()
        if fp_set != filepath_set:
            MigrationRecord.objects.create(mid=mid, content=compress_files(root_dir, path_set=filepath_set))
            pk_list = queryset.values_list('pk', flat=True)
            if settings.DEKDJSELFMIGRATION_UP_LIMIT:
                pk_list = pk_list[settings.DEKDJSELFMIGRATION_UP_LIMIT:]
            queryset.filter(
                pk__in=pk_list
            ).delete()
