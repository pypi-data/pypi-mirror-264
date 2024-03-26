from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import Menu, SubmenuMenuItem
from wagtail.contrib.settings.registry import SettingMenuItem
from wagtail import hooks

from ..options import (
    MENU_ITEM_REGISTER_HOOK_NAME,
)
from ..models import (
    UIImprovementSettings,
    MetaTags,
)


wagtail_themes_menu = Menu(
    register_hook_name="register_wagtail_themes_menu_item",
    construct_hook_name="construct_wagtail_themes_menu",
)


@hooks.register("register_wagtail_themes_menu_item")
def register_wagtail_themes_menu_item():
    return SettingMenuItem(
        model=UIImprovementSettings,
        icon="draft",
        order=1000,
    )


@hooks.register("register_wagtail_themes_menu_item")
def register_meta_tags_menu_item():
    return SettingMenuItem(
        model=MetaTags,
        icon="tag",
        order=2000,
    )


@hooks.register(MENU_ITEM_REGISTER_HOOK_NAME)
def register_settings_menu_item():
    return SubmenuMenuItem(
        _("UI Improvements"),
        menu=wagtail_themes_menu,
        name="wagtail_themes_settings_menu",
        icon_name="sliders",
        order=1000,
    )
