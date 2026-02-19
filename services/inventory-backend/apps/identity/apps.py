from django.apps import AppConfig


class AuthHistoryRecordsMixin:
    """Enforce db_table naming for auth m2m history models."""

    def get_meta_options_m2m(self, through_model):
        meta_fields = super().get_meta_options_m2m(through_model)
        if through_model._meta.db_table == "auth_group_permissions":
            meta_fields["db_table"] = "hist_auth_group_permissions"
        return meta_fields


class IdentityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.identity"
    verbose_name = "Identity"

    def ready(self) -> None:
        from django.contrib.auth.models import Group, Permission
        from simple_history.models import HistoricalRecords
        from simple_history import register
        from simple_history.exceptions import MultipleRegistrationsError

        class AuthHistoricalRecords(AuthHistoryRecordsMixin, HistoricalRecords):
            pass

        try:
            register(
                Group,
                app="apps.identity",
                records_class=AuthHistoricalRecords,
                table_name="hist_auth_group",
                m2m_fields=["permissions"],
            )
        except MultipleRegistrationsError:
            pass

        try:
            register(
                Permission,
                app="apps.identity",
                table_name="hist_auth_permission",
            )
        except MultipleRegistrationsError:
            pass
