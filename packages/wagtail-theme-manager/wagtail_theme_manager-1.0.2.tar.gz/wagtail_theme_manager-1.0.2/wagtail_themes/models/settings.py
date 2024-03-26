from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, HelpPanel, TabbedInterface, ObjectList, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.fields import StreamField

from globlocks.fields import (
    FontField,
)
from ..blocks import (
    settings as settings_blocks,
)
from ..settings_registry import register_without_menu_item as register_setting


class UIImprovementStreamField(StreamField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_block.set_name("UIImprovementStreamField")

    def _to_python(self, value):
        return self.stream_block.to_python(value)
    
    def get_prep_value(self, value):
        return self.stream_block.get_prep_value(value)



@register_setting
class UIImprovementSettings(BaseGenericSetting):
    select_related = ["logo"]

    logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        help_text=_("The logo to use for the site"),
        verbose_name=_("Logo"),
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The title of the site (Also used as copyright label)"),
        verbose_name=_("Title"),
    )

    font = FontField(
        blank=False,
        null=False,
        verbose_name=_("Font"),
        help_text=_("The font to use for the site"),
    )

    styles = UIImprovementStreamField(
        settings_blocks.SiteStyles,
        blank=False,
        null=False,
        min_num=1,
        max_num=1,
        verbose_name=_("Styles"),
        help_text=_("Custom styles for the site"),
    )

    components = UIImprovementStreamField(
        settings_blocks.SiteComponents,
        blank=False,
        null=False,
        min_num=1,
        max_num=1,
        verbose_name=_("Components"),
        help_text=_("Custom components for the site"),
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("Last Updated"),
    )

    general_panels_handler = [
        FieldPanel("logo"),
        FieldPanel("title"),
        FieldPanel("font"),
        FieldPanel("last_updated", read_only=True),
    ]

    style_panels_handler = [
        FieldPanel("styles"),
    ]

    components_panels_handler = [
        FieldPanel("components"),
    ]


    edit_handler = TabbedInterface([
        ObjectList(general_panels_handler, heading=_("General")),
        ObjectList(style_panels_handler, heading=_("Styles")),
        ObjectList(components_panels_handler, heading=_("Components")),
    ])


    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

