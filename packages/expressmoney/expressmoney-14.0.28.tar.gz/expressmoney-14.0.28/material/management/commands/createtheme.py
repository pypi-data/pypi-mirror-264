import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import material
from ... import compat


class Command(BaseCommand):
    help = "Generates new theme for django-material"

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--primary-color', action='store', dest='primary_color', default='424242',
            help="Primary theme color")
        parser.add_argument(
            '--secondary-color', action='store', dest='secondary_color', default='424242',
            help="Secondary theme color")
        parser.add_argument(
            '--dest', action='store', dest='destination', nargs='?',
            help="Destination directory"
        )

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        dest_dir = options['destination']
        if dest_dir is None:
            if settings.STATICFILES_DIRS:
                dest_dir = settings.STATICFILES_DIRS[0]

        if self.verbosity >= 1:
            print('Output directory: {}/material/css'.format(dest_dir))

        if not os.path.exists(os.path.join(dest_dir, 'material', 'imgs')):
            os.makedirs(os.path.join(dest_dir, 'material', 'imgs'))
        if not os.path.exists(os.path.join(dest_dir, 'material', 'css')):
            os.makedirs(os.path.join(dest_dir, 'material', 'css'))

        build_dir = self.prepare_build_dir()
        self.install_packages(build_dir)
        self.gulp(build_dir, dest_dir, options)

    def prepare_build_dir(self):
        build_dir = os.path.join(settings.BASE_DIR, '.material')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        package_dir = os.path.join(material.__path__[0], 'conf', 'theme_generator')
        for filename in os.listdir(package_dir):
            shutil.copy(os.path.join(package_dir, filename), build_dir)

        return build_dir

    def install_packages(self, build_dir):
        cmd = compat.which('yarn')
        if cmd is None:
            raise CommandError("To create a theme you need to have 'yarn' tool installed.")

        args = [cmd, 'install']
        with compat.Popen(args, cwd=build_dir) as process:
            try:
                return process.wait()
            except:
                process.kill()
                process.wait()
                raise

    def gulp(self, build_dir, dest_dir, options):
        package_dir = material.__path__[0]

        args = [
            'npm', 'run', 'gulp', '--',
            '--dst', dest_dir,
            '--src', package_dir,
            '--primary-color', options['primary_color'],
            '--secondary-color', options['secondary_color']
        ]

        with compat.Popen(args, cwd=build_dir) as process:
            try:
                return process.wait()
            except:
                process.kill()
                process.wait()
                raise
