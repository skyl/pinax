from django.http import HttpResponse, Http404
from django.db.models import get_model

from django.contrib.contenttypes.models import ContentType

from tagging.models import Tag


def autocomplete(request, app_label=None, model=None):

    # get the relevent model if applicable
    if app_label and model:
        try:
            model = ContentType.objects.get(app_label=app_label, model=model)
        except:
            raise Http404
    else:
        model = None
    
    if not request.GET.has_key("q"):
        raise Http404
    else:
        q = request.GET["q"]
    
    # counts can be 'all', 'model' or 'None'
    counts = request.GET.get("counts", "all")
    limit = request.GET.get("limit", 10)
    
    if model:
        tags = Tag.objects.filter(
            items__content_type = model,
            name__istartswith = q
        ).distinct()[:limit]
    else:
        tags = Tag.objects.filter(
            name__istartswith = q
        ).distinct()[:limit]

    if counts == "all":
        l = sorted(list(tags),
            lambda x, y: cmp(y.items.all().count(), x.items.all().count())
        )
        tag_list = "\n".join([ '%s||(%s)' % (tag.name, tag.items.all().count() ) for tag in l if tag])

    elif counts == "model":
        if model:
            l = sorted(list(tags),
                lambda x, y:
                    cmp(y.items.filter(content_type=model).count(), x.items.filter(content_type=model).count())
            )
            tag_list = "\n".join(
                ["%s||(%s)" % (tag.name, tag.items.filter(content_type=model).count()) for tag in l if tag]
            )
        else:
            raise Exception(
                'You asked for a model with GET but did not pass one to the url'
            )
    else:
        tag_list = "\n".join([tag.name for tag in tags if tag])
    return HttpResponse(tag_list)
