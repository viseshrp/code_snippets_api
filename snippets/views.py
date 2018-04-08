from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
# custom permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import renderers


# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {  # reverse - returns complete URLs
            'users': reverse('snippet-list', request=request, format=format),
            'snippets': reverse('user-list', request=request, format=format)
        }
    )


class SnippetList(generics.ListCreateAPIView):
    """
    list all snippets or create new.

    ListCreateAPIView is an even more abstracted view that implements
    mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView.
    As we had done in views_mixins.py.

    These are already mixed in generic views.

    So, even lesser code. This is fucking awesome!
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # when snippet is created, no way of associating user with
    # created snippet. User is not part of the serialized snippet
    # representation. The data passed to SnippetSerializer(data=request.data)
    # only has the data from the request. The actual user is a property
    # of the incoming request, and is accessed as request.user

    # Override perform_create. Used to modify how the instance save
    # is done. This method is used in CreateModelMixin as
    # serializer.save(). If you need to save extra fields, add them
    # as arguments to the save call.
    # These fields need to be explicitly saved, in addition to the
    # actual serialized validated data.
    # also need to update the actual snippet serializer after this.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # set permissions. If authenticated - read write access.
    # else read only
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, delete, modify snippet

    Code snippets are always associated with a creator.
    Only authenticated users may create snippets.
    Only the creator of a snippet may update or delete it.
    Unauthenticated requests should have full read-only access.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # set permissions. If authenticated - read write access.
    # else read only
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    """
    list all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    detail of a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
