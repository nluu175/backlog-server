import json
from django.core.management.base import BaseCommand
from ...models.Genre import Genre


import os

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, "genres_list.json")


class Command(BaseCommand):
    help = "Import genres from a JSON file"

    def handle(self, *args, **kwargs):
        with open(file_path, "r") as data_file:
            data = json.load(data_file)
            for item in data:
                name = item["name"]

                code = name.lower().replace(" ", "-")
                genre, created = Genre.objects.get_or_create(
                    name=name, defaults={"code": code}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created genre "{name}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Genre "{name}" already exists')
                    )
