from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics


# Create your views here.

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    list all snippets or create new.

    base class GenericAPIView provides core functionality.
    mixins provide list and create methods.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # args, kwargs are the primary key and the other url params
    # passed with the url.
    
    # bind get to list action
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # bind post to create action
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Read, delete, modify snippet
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
