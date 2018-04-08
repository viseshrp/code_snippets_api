# to serialize and deserialize model instances
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.ModelSerializer):
    # after associating user to snippets and overriding saving of snippets
    # to accomodate for users.
    owner = serializers.ReadOnlyField(source='owner.username')

    # in source='owner.username', owner is the name of the snippet-user
    #  relationship in the snippet model. username is the field of User model
    # which is used as a parameter while serializing or deserializing the snippet
    # model. say for printing purposes.
    # 'source' controls which attribute is used to populate the owner
    # field, can be any property of User model.
    # source='owner.username' will try to print owner and then the username field
    # associated with the owner.

    # can use ReadOnlyField or CharField(read_only=True)

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style',
                  'owner')

    # modelserializers have default implementations of create and update.


class UserSerializer(serializers.ModelSerializer):
    """
    add representations of users to our API
    """
    # user serializer uses the user model fields to serialize by default
    # but additional fields have to be serialized explicitly.
    # snippets is a reverse relation to User model.
    # owner field in Snippets model is a relationship
    # snippets field here is a reverse relationship between User
    # and Snippet model
    #
    # PrimaryKeyRelatedField - used to refer to the other side
    # of the relationship that is using (current side)/User's primary key
    # in this case, snippet model is using User's primary key

    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    # this field can either be read only or read write
    # if readonly, apis wont allow requests to change it,
    # set read_only=True in above line.
    # if read write, changes are allowed, but you have to mention the
    # queryset that will be used to validate the field input when api
    # is trying to write to it.

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
