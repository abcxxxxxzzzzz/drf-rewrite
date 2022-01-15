import django_filters

from .models import DmModel


class DmModelFilter(django_filters.rest_framework.FilterSet):
    """
    域名组过滤类
    """
    domain = django_filters.CharFilter(lookup_expr="icontains")
    group = django_filters.NumberFilter(method="search_group")

    def search_group(self, queryset, name, value):
        return queryset.filter(group__pk=value)


    class Meta:
        model  = DmModel
        fields = ['domain', 'group']