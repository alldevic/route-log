from django_filters import rest_framework

from reports.models import ContainerUnloadFact, Report


class ContainerUnloadFactFilter(rest_framework.FilterSet):
    class Meta:
        model = ContainerUnloadFact
        fields = {
            'report': ['exact'],
            'value': ['exact'],
            'is_unloaded': ['exact'],
            'directory': ['exact', 'contains']
        }


class ReportFilter(rest_framework.FilterSet):
    class Meta:
        model = Report
        fields = {
            'device': ['exact'],
            'date': ['exact'],
        }
