from django.conf import settings
from django.core.management.commands import dumpdata
# from django.core.management.base import CommandError

from datetime import datetime
from os import path, makedirs, remove
from time import sleep

from rahavard import (
    get_list_of_files,
    to_tilda,
)


## https://stackoverflow.com/a/37755287/14388247
class Command(dumpdata.Command):
    help = 'My Customized Version of the Original dumpdata Command'

    ## https://stackoverflow.com/a/78204755/14388247
    def __init__(self, *args, **kwargs):
        kwargs['no_color'] = not kwargs.get('force_color', False)
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):

        ## dump --------------

        print('>>> Running customized dumpdata\n')

        dest_dir = f'{settings.PROJECT_DIR}/dumped'
        if not path.exists(dest_dir):
            print(f'creating {dest_dir}')
            makedirs(dest_dir)

        ## include app slug (if any) in output_file
        apps_string = ''
        if args:
            if len(args) == 1:
                apps_string = '--app-'
            else:
                apps_string = '--apps-'

            for _ in args:
                apps_string = f'{apps_string}{_}-'
            apps_string = apps_string.rstrip('-')

        ymdhms = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        extension = 'json'

        output_file = f'{dest_dir}/{settings.HOST_NAME}-{ymdhms}{apps_string}.{extension}'
        print(f'dumping to: {to_tilda(output_file)}')

        ## commented because caused errors
        # -e contenttypes -e auth.Permission

        options['format'] = extension
        options['indent'] = 2
        options['skip_checks'] = True
        options['output'] = output_file
        options['use_natural_foreign_keys'] = True
        options['use_natural_primary_keys'] = True
        options['verbosity'] = 3
        # --all

        super().handle(*args, **options)


        ## rotate --------------

        print('getting list of already dumped files')
        dumped_files = get_list_of_files(directory=dest_dir, extension=extension)
        print(f'  count: {len(dumped_files)}')

        LAST_DUMPED_FILES_TO_SKIP = 240  ## last n dumped_files to skip removing
        to_be_removed = dumped_files[:-LAST_DUMPED_FILES_TO_SKIP]

        if to_be_removed:
            to_be_removed__len = len(to_be_removed)
            print(f'{to_be_removed__len} to be removed:')
            for idx, tbr in enumerate(to_be_removed, start=1):
                print(f' {idx}/{to_be_removed__len}: removing {tbr}')
                remove(tbr)
                sleep(.1)
