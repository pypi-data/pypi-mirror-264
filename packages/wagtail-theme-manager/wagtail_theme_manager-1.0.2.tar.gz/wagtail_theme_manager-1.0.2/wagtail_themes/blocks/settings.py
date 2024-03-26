from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from globlocks.blocks import (
    ColorBlock,
    RangeSliderBlock,
)


def color_blocks(
        theme: str,
        suffix="",
        default_text_color: str = "#000000",
        default_bg_color: str = "#FFFFFF",
        theme_help_format: str = _("The %(theme)s %(applied_to)s color of the block"),
        theme_label_format: str = _("%(theme)s %(applied_to)s"),
    ):
    """Return a tuple of color blocks for a theme."""

    if suffix:
        suffix = f"_{suffix}" if not suffix.endswith("_") else suffix

    return (
        (f"bg{suffix}", ColorBlock(
            required=True,
            help_text=theme_help_format % {"theme": theme, "applied_to": _("background")},
            label=theme_label_format % {"theme": theme, "applied_to": _("Background")},
            default=default_bg_color,
        )),
        (f"text{suffix}", ColorBlock(
            required=True,
            help_text=theme_help_format % {"theme": theme, "applied_to": _("text")},
            label=theme_label_format % {"theme": theme, "applied_to": _("Text")},
            default=default_text_color,
        )),
    )


class StyleBlock(blocks.StructBlock):
    """Style block."""

    bg = blocks.Block()
    bg_hover = blocks.Block()
    bg_active = blocks.Block()
    
    text = blocks.Block()
    text_hover = blocks.Block()
    text_active = blocks.Block()

    def __init__(self, local_blocks = None, theme: str = None, default_text_color: str = "#000000", default_bg_color: str = "#FFFFFF", *args, **kwargs):
        if local_blocks is None:
            local_blocks = ()

        if not theme:
            raise ValueError("theme is required")

        for suffix in ("", "hover", "active"):

            theme_help_format = _("The %(theme)s %(applied_to)s color of the block")
            theme_label_format = _("%(theme)s %(applied_to)s")

            if suffix:
                theme_help_format = _(f"The %(theme)s %(applied_to)s color of the block on {suffix}")
                theme_label_format = _(f"%(theme)s %(applied_to)s on {suffix}")

            blocks = color_blocks(
                theme,
                suffix,
                default_text_color,
                default_bg_color,
                theme_help_format,
                theme_label_format,
            )
            local_blocks += blocks

        super().__init__(local_blocks, *args, **kwargs)


class BaseUIImprovementBlock(blocks.StructBlock):
    MUTABLE_META_ATTRIBUTES = [
        "max_num", "min_num", "required", "help_text", "label", "default"
    ]


class SiteStyles(BaseUIImprovementBlock):
    # Colors
    primary = StyleBlock(
        theme=_("Primary"),
        default_text_color="#FFFFFF",
        default_bg_color="#007bff",
        form_classname="ui-improvements-primary collapsible",
    )
    secondary = StyleBlock(
        theme=_("Secondary"),
        default_text_color="#FFFFFF",
        default_bg_color="#6c757d",
        form_classname="ui-improvements-secondary collapsible",
    )
    info = StyleBlock(
        theme=_("Info"),
        default_text_color="#FFFFFF",
        default_bg_color="#17a2b8",
        form_classname="ui-improvements-info collapsible",
    )
    success = StyleBlock(
        theme=_("Success"),
        default_text_color="#FFFFFF",
        default_bg_color="#28a745",
        form_classname="ui-improvements-success collapsible",
    )
    warning = StyleBlock(
        theme=_("Warning"),
        default_text_color="#FFFFFF",
        default_bg_color="#ffc107",
        form_classname="ui-improvements-warning collapsible",
    )
    danger = StyleBlock(
        theme=_("Danger"),
        default_text_color="#FFFFFF",
        default_bg_color="#dc3545",
        form_classname="ui-improvements-danger collapsible",
    )
    light = StyleBlock(
        theme=_("Light"),
        default_text_color="#212529",
        default_bg_color="#f8f9fa",
        form_classname="ui-improvements-light collapsible",
    )
    dark = StyleBlock(
        theme=_("Dark"),
        default_text_color="#FFFFFF",
        default_bg_color="#343a40",
        form_classname="ui-improvements-dark collapsible",
    )

class SiteComponents(BaseUIImprovementBlock):
    link = StyleBlock(
        theme=_("Link"),
        default_text_color="#007bff",
        default_bg_color="transparent",
    )
    border_thickness = RangeSliderBlock(
        required=True,
        help_text=_("The thickness of the border"),
        label=_("Border Thickness"),
        unit="px",
        min_value=0,
        max_value=10,
        default=1,
    )
    border_radius = RangeSliderBlock(
        required=True,
        help_text=_("The radius of the border"),
        label=_("Border Radius"),
        unit="px",
        min_value=0,
        max_value=50,
        default=0,
    )

