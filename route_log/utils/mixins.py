from rest_framework.response import Response


class DynamicListModelMixin:
    """
    Применим к view которые унаследованы от :class:`~core.utils.serializers.DynamicFieldsModelSerializer`
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = request.query_params.get('fields', None)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, fields=fields, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, fields=fields, many=True)
        return Response(serializer.data)


class DynamicRetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        fields = request.query_params.get('fields', None)

        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=fields)
        return Response(serializer.data)
