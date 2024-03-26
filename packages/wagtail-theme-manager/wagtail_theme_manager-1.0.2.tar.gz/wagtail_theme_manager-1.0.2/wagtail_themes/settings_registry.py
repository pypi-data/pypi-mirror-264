from wagtail.contrib.settings.registry import registry, GenericSettingAdminURLFinder, SiteSettingAdminURLFinder
from django.contrib.auth.models import Permission
from wagtail import hooks
from wagtail.admin.admin_url_finder import (
    register_admin_url_finder,
)
from wagtail.permission_policies import ModelPermissionPolicy
from wagtail.contrib.settings.registry import SettingMenuItem as WagtailSettingsMenuItem


def get_menu_item(model, icon="", **kwargs):
    return WagtailSettingsMenuItem(
        model=model,
        icon=icon,
        **kwargs,
    )

def register_without_menu_item(model=None):
    """
    Register a model as a setting, without adding it to the wagtail admin menu
    """
    if model is None:
        return lambda model: _register(model)
    return _register(model)

def _register(model, **kwargs):
    from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting

    if model in registry:
        return model
    registry.append(model)

    @hooks.register("register_permissions")
    def permissions_hook():
        return Permission.objects.filter(
            content_type__app_label=model._meta.app_label,
            codename=f"change_{model._meta.model_name}",
        )

    # Register an admin URL finder
    permission_policy = ModelPermissionPolicy(model)

    if issubclass(model, BaseSiteSetting):
        finder_class = type(
            "_SiteSettingAdminURLFinder",
            (SiteSettingAdminURLFinder,),
            {"model": model, "permission_policy": permission_policy},
        )
    elif issubclass(model, BaseGenericSetting):
        finder_class = type(
            "_GenericSettingAdminURLFinder",
            (GenericSettingAdminURLFinder,),
            {"model": model, "permission_policy": permission_policy},
        )
    else:
        raise NotImplementedError

    register_admin_url_finder(model, finder_class)

    return model

