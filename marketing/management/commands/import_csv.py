import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from marketing.models import CustomerPrediction
from marketing.ml_utils import predict_result


def normalize_field_name(name: str) -> str:
    return name.strip().lower().replace(' ', '').replace('-', '').replace('.', '')


class Command(BaseCommand):
    help = 'Import customer prediction rows from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file to import.')
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update an existing record when the CSV row contains an id column.',
        )
        parser.add_argument(
            '--no-predict',
            action='store_true',
            help='Do not compute prediction_result; use CSV value if provided or leave blank.',
        )

    def handle(self, *args, **options):
        csv_path = Path(options['csv_path'])
        if not csv_path.exists():
            raise CommandError(f'CSV file not found: {csv_path}')

        model_fields = [
            field.name
            for field in CustomerPrediction._meta.get_fields()
            if getattr(field, 'concrete', False) and not field.auto_created
        ]

        field_map = {normalize_field_name(name): name for name in model_fields}
        field_map['id'] = 'id'
        input_fields = [
            name for name in model_fields if name not in {'prediction_result', 'created_at'}
        ]
        id_field = 'id'

        created = 0
        updated = 0
        skipped = 0

        with csv_path.open(newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames is None:
                raise CommandError('CSV file appears to be empty or malformed.')

            for row_number, row in enumerate(reader, start=1):
                normalized_row = {
                    field_map.get(normalize_field_name(key), key): value.strip()
                    for key, value in row.items()
                    if value is not None and value.strip() != ''
                }

                existed = False
                if options['update_existing'] and normalized_row.get(id_field):
                    try:
                        record = CustomerPrediction.objects.get(pk=normalized_row[id_field])
                        existed = True
                    except CustomerPrediction.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'Row {row_number}: id={normalized_row[id_field]} not found, creating new record.'
                        ))
                        record = CustomerPrediction()
                else:
                    record = CustomerPrediction()

                for field in input_fields:
                    if field in normalized_row:
                        setattr(record, field, normalized_row[field])

                if not options['no_predict']:
                    try:
                        prediction_source = {
                            field: getattr(record, field)
                            for field in input_fields
                            if getattr(record, field) is not None
                        }
                        record.prediction_result = predict_result(prediction_source)
                    except Exception as exc:
                        self.stderr.write(
                            f'Row {row_number}: failed to compute prediction_result: {exc}'
                        )
                        record.prediction_result = normalized_row.get('prediction_result', '')
                else:
                    record.prediction_result = normalized_row.get('prediction_result', '')

                record.save()
                if existed:
                    updated += 1
                else:
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Import complete: {created} created, {updated} updated, {skipped} skipped.'
        ))
