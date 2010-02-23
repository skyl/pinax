from django import template

register = template.Library()

@register.inclusion_tag('tagging_utils/tag_autocomplete_js.html')
def tag_autocomplete_js(app_label, model, counts=None):
    """Counts may be 'all' or 'model' """
    return {
        'app_label': app_label, 'model': model, 'counts': counts
    }


