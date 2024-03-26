from django.conf import settings


MENU_ITEM_REGISTER_HOOK_NAME = getattr(
    settings,
    "wagtail_themes_MENU_ITEM_REGISTER_HOOK_NAME",
    "register_settings_menu_item",
)
