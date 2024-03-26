from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import Block
from wagtail.fields import StreamField
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
)

from ..settings_registry import register_without_menu_item as register_setting
from ..blocks import MetaTagBlock


@register_setting
class MetaTags(BaseSiteSetting):

    tags = StreamField([
        ("meta", MetaTagBlock()),
    ], blank=True, null=True, verbose_name=_("Meta Tags"), use_json_field=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("tags"),
        ], heading=_("Meta Tags"), help_text=mark_safe(_(
            "<pre>Meta tags to be included in the <head> of the page.\n"
            "This can be used to add custom meta tags, such as OpenGraph tags.\n"
            "Note: These tags are not validated, so be careful!</pre>"
            "<a href=\"https://ogp.me/\" target=\"_blank\">OpenGraph Meta Tags</a> "
            "<a href=\"https://www.w3schools.com/tags/tag_meta.asp\" target=\"_blank\">W3 Meta Tags</a>"
        ))),
    ]


    class Meta:
        verbose_name = _("Meta Tags")
        verbose_name_plural = _("Meta Tags")

    def render_as_block(self, context=None):
        context = context or {}
        context["self"] = self
        context[Block.TEMPLATE_VAR] = self

        return render_to_string(
            "wagtail_themes/metatags/metatags.html",
            context=context,
            request=context.get(
                "request", None,
            ),
        )
