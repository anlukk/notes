from datetime import datetime
from unicodedata import category
from django.db.models import Q


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = category.objects.all()
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
    


def archive_unnecessary_records(model):
    """
    Moves unnecessary records to an archive and removes them from the archive page.
    :param model: The model class to archive records from.
    """
    archive_criteria = Q(archived=False) & Q(date__lt=datetime.date.today() - datetime.timedelta(days=30))
    records_to_archive = model.objects.filter(archive_criteria)
    records_to_archive.update(archived=True)
    queryset = model.objects.exclude(archived=True)
    return queryset