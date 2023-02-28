from unicodedata import category


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = category.objects.all()
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context