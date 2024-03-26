from globlocks.blocks import BaseBlock, BaseBlockConfiguration
from django.utils.translation import gettext_lazy as _
from django import forms
from wagtail import blocks


class MetaTagBlockConfiguration(BaseBlockConfiguration):
    custom_html_element = blocks.CharBlock(
        required=False,
        label=_("Custom HTML Element"),
    )


class MetaTagBlock(BaseBlock):
    """Meta tag block."""

    advanced_settings_class = MetaTagBlockConfiguration

    property_name = blocks.CharBlock(required=False)
    property_value = blocks.CharBlock(required=False)
    content = blocks.CharBlock(required=False)

    class Meta:
        template = "wagtail_themes/metatags/metatag.html"
        icon = "bookmark"
        label = _("Meta Tag")

    def clean(self, value):
        value = super().clean(value)
        settings = self.get_settings(value)
        custom_html_element = settings.get("custom_html_element", "")
        if custom_html_element:
            return value
        if not value.get("property_name", ""):
            raise forms.ValidationError(_("Property name is required"))
        if not value.get("property_value", ""):
            raise forms.ValidationError(_("Property name is required"))
        return value
