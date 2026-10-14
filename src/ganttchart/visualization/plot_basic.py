
# Text management functions for matplotlib
def FormatText(Text, fontsize=None, Weight=None, Style=None, Family=None,
                Color=None, BackgroundColor=None, Alpha=None):
    """
    Applies text formatting options dynamically.
    If an option is None, it resets to the default Matplotlib setting.
    
    Args:
        Text: Matplotlib text object
        fontsize: float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        Weight: {'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'}
        Style: {'normal', 'italic', 'oblique'} or None
        Family: {'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'} or None
        Color: Named Color, hex ('#FF5733'), or RGB tuple ((1,0,0))
        BackgroundColor: Same as Color
        Alpha: float (0.0 to 1.0, where 0 is fully transparent and 1 is opaque)
    """
    if fontsize is not None:
        Text.set_fontsize(fontsize)

    if Weight is not None:
        Text.set_weight(Weight)

    if Style is not None:
        Text.set_style(Style)

    if Family is not None:
        Text.set_family(Family)

    if Color is not None:
        Text.set_color(Color)

    if BackgroundColor is not None:
        Text.set_backgroundcolor(BackgroundColor)

    if Alpha is not None:
        Text.set_alpha(Alpha)