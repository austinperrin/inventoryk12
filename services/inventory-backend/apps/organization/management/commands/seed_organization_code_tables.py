from collections.abc import Sequence

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.organization.models import OrganizationCode
from apps.organization.seeds import ORGANIZATION_CODE_SEEDS

ORGANIZATION_CODE_TABLE_SEEDS = (("OrganizationCode", OrganizationCode, ORGANIZATION_CODE_SEEDS),)


class Command(BaseCommand):
    help = "Seed baseline system-managed organization code-table values."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview the seed changes without writing to the database.",
        )

    def handle(self, *args, **options) -> None:
        dry_run: bool = options["dry_run"]

        with transaction.atomic():
            for model_name, model, rows in ORGANIZATION_CODE_TABLE_SEEDS:
                created_count, updated_count = self._seed_model(model, rows, dry_run=dry_run)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{model_name}: created={created_count} updated={updated_count}"
                    )
                )

            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("Dry run complete; no changes written."))

    def _seed_model(
        self, model, rows: Sequence[dict[str, object]], *, dry_run: bool
    ) -> tuple[int, int]:
        created_count = 0
        updated_count = 0

        for row in rows:
            defaults = {
                "label": row["label"],
                "description": row.get("description", ""),
                "sort_order": row["sort_order"],
                "is_system_managed": True,
                "is_active": True,
            }

            instance, created = model.objects.update_or_create(
                local_id=row["local_id"],
                defaults={
                    "code": row["code"],
                    **defaults,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            if dry_run:
                instance.refresh_from_db()

        return created_count, updated_count
