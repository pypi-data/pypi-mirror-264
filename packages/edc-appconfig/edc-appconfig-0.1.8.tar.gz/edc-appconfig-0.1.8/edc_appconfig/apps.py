import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.checks import register
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
from edc_action_item.post_migrate_signals import update_action_types
from edc_action_item.site_action_items import site_action_items
from edc_action_item.system_checks import edc_action_item_checks
from edc_auth.post_migrate_signals import post_migrate_user_groups_and_roles
from edc_auth.site_auths import site_auths
from edc_consent.site_consents import site_consents
from edc_data_manager.post_migrate_signals import (
    populate_data_dictionary,
    update_query_rule_handlers,
)
from edc_data_manager.site_data_manager import site_data_manager
from edc_export.system_checks import edc_export_checks
from edc_facility.system_checks import holiday_country_check, holiday_path_check
from edc_form_runners.site import site_form_runners
from edc_lab.post_migrate_signals import update_panels_on_post_migrate
from edc_lab.site_labs import site_labs
from edc_list_data.post_migrate_signals import post_migrate_list_data
from edc_list_data.site_list_data import site_list_data
from edc_metadata.metadata_rules import site_metadata_rules
from edc_metadata.system_checks import check_for_metadata_rules
from edc_navbar.site_navbars import site_navbars
from edc_navbar.system_checks import edc_navbar_checks
from edc_notification.post_migrate_signals import post_migrate_update_notifications
from edc_notification.site_notifications import site_notifications
from edc_pdutils.site_values_mappings import site_values_mappings
from edc_prn.site_prn_forms import site_prn_forms
from edc_randomization.site_randomizers import site_randomizers
from edc_reportable.site_reportables import site_reportables
from edc_sites.post_migrate_signals import post_migrate_update_sites
from edc_sites.site import sites as site_sites
from edc_sites.system_checks import sites_check
from edc_visit_schedule.post_migrate_signals import populate_visit_schedule
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.system_checks import (
    check_form_collections,
    check_onschedule_exists_in_subject_schedule_history,
    check_subject_schedule_history,
    visit_schedule_check,
)
from multisite.apps import post_migrate_sync_alias

style = color_style()

__all__ = ["AppConfig"]


class AppConfig(DjangoAppConfig):
    """AppConfig class for main EDC apps.py.

    Should be the last app in INSTALLED_APPS

    The post_migrate signal(s) registered here will
    find site globals fully populated.

    For example,
    'post_migrate_user_groups_and_roles' needs site_consents
    to be fully populated before running.
    """

    name = "edc_appconfig"
    verbose_name = "Edc AppConfig"
    has_exportable_data = False
    include_in_administration_section = False

    def ready(self):
        sys.stdout.write("Loading edc_appconfig ...\n")
        self.call_autodiscovers()
        self.register_system_checks()
        self.register_post_migrate_signals()
        sys.stdout.write("Done loading edc_appconfig.\n")

    @staticmethod
    def call_autodiscovers():
        """Call autodiscover on apps to load globals"""
        site_consents.autodiscover()
        site_auths.autodiscover()
        site_sites.autodiscover()
        site_reportables.autodiscover()
        site_labs.autodiscover()
        site_list_data.autodiscover()
        site_action_items.autodiscover()
        site_data_manager.autodiscover()
        site_notifications.autodiscover()
        # site_offline_models.autodiscover()
        # site_model_callers.autodiscover()
        site_form_runners.autodiscover()
        site_metadata_rules.autodiscover()
        site_visit_schedules.autodiscover()
        site_navbars.autodiscover()
        site_values_mappings.autodiscover()
        site_prn_forms.autodiscover()
        site_randomizers.autodiscover()

    @staticmethod
    def register_system_checks():
        """Register system checks"""
        from edc_consent.system_checks import check_consents  # wait, app not ready

        sys.stdout.write(" * registering system checks\n")
        sys.stdout.write("   - visit_schedule_check\n")
        register(visit_schedule_check)
        sys.stdout.write("   - check_form_collections\n")
        register(check_form_collections)
        sys.stdout.write("   - check subject schedule history\n")
        register(check_subject_schedule_history, deploy=True)
        sys.stdout.write("   - check onschedule with subject schedule history\n")
        register(check_onschedule_exists_in_subject_schedule_history)
        sys.stdout.write("   - edc_action_item_checks\n")
        register(edc_action_item_checks)
        sys.stdout.write("   - sites_check\n")
        register(sites_check)
        sys.stdout.write("   - edc_export_checks\n")
        register(edc_export_checks, deploy=True)
        sys.stdout.write("   - holiday_path_check (deploy only)\n")
        register(holiday_path_check, deploy=True)
        sys.stdout.write("   - holiday_country_check (deploy only)\n")
        register(holiday_country_check, deploy=True)
        sys.stdout.write("   - check_for_metadata_rules (deploy only)\n")
        register(check_for_metadata_rules)
        sys.stdout.write("   - check_site_consents\n")
        register(check_consents)
        sys.stdout.write("   - edc_navbar_checks\n")
        register(edc_navbar_checks)

    def register_post_migrate_signals(self):
        """Register post-migrate signals."""
        sys.stdout.write(" * registering post-migrate signals ...\n")
        sys.stdout.write("   - post_migrate.populate_visit_schedule\n")
        post_migrate.connect(
            populate_visit_schedule,
            sender=self,
            dispatch_uid="edc_visit_schedule.populate_visit_schedule",
        )
        sys.stdout.write("   - post_migrate.post_migrate_update_sites\n")
        post_migrate.connect(
            post_migrate_update_sites,
            sender=self,
            dispatch_uid="edc_sites.post_migrate_update_sites",
        )
        sys.stdout.write("   - post_migrate.multisite.post_migrate_sync_alias\n")
        if (
            "multisite" in settings.INSTALLED_APPS
            or "multisite.apps" in settings.INSTALLED_APPS
        ):
            post_migrate.connect(
                post_migrate_sync_alias,
                sender=self,
                dispatch_uid="multisite.post_migrate_sync_alias",
            )
        sys.stdout.write("   - post_migrate.update_panels_on_post_migrate\n")
        post_migrate.connect(
            update_panels_on_post_migrate,
            sender=self,
            dispatch_uid="edc_lab.update_panels_on_post_migrate",
        )
        sys.stdout.write("   - post_migrate.post_migrate_list_data\n")
        post_migrate.connect(
            post_migrate_list_data,
            sender=self,
            dispatch_uid="edc_list_data.post_migrate_list_data",
        )
        sys.stdout.write("   - post_migrate.update_action_types\n")
        post_migrate.connect(
            update_action_types,
            sender=self,
            dispatch_uid="edc_action_item.update_action_types",
        )
        sys.stdout.write("   - post_migrate.post_migrate_user_groups_and_roles\n")
        post_migrate.connect(
            post_migrate_user_groups_and_roles,
            sender=self,
            dispatch_uid="edc_auth.post_migrate_user_groups_and_roles",
        )
        sys.stdout.write("   - post_migrate.update_query_rule_handlers\n")
        post_migrate.connect(
            update_query_rule_handlers,
            sender=self,
            dispatch_uid="edc_data_manager.update_query_rule_handlers",
        )
        sys.stdout.write("   - post_migrate.populate_data_dictionary\n")
        post_migrate.connect(
            populate_data_dictionary,
            sender=self,
            dispatch_uid="edc_data_manager.populate_data_dictionary",
        )
        sys.stdout.write("   - post_migrate.post_migrate_update_notifications\n")
        post_migrate.connect(
            post_migrate_update_notifications,
            sender=self,
            dispatch_uid="edc_notification.post_migrate_update_notifications",
        )
