from django_filters import rest_framework

from reports.models import ContainerUnloadFact


class ContainerUnloadFactFilter(rest_framework.FilterSet):
    class Meta:
        model = ContainerUnloadFact
        fields = {
            'report': ['exact'],
        }
