"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import logging
from django.contrib import admin
from django.urls import path, re_path
from graphene_django.views import GraphQLView
import six  # required by GraphQLView default formatter
from graphql import GraphQLError

logger = logging.getLogger(__name__)


class PkgGraphQLView(GraphQLView):
    """
    This class exists for overriding the error formatting method in GraphQLView.
    """

    @staticmethod
    def format_error(error):
        """
        Override the error formatting method in GraphQL View.
        :param error: error instance in GraphQLView response
        :return: formatted error in dictionary
        """
        def format_graphql_error(error):
            """
            The formatter for GraphQLError
            :param error: error instance in GraphQLView response
            :return: formatted error in dictionary
            """
            formatted_error = {
                'message': str(error),
            }

            # If error is a server-end error, report the specific type
            if hasattr(error, 'original_error'):
                formatted_error['type'] = type(error.original_error).__name__

            if isinstance(error, GraphQLError):
                if error.locations is not None:
                    formatted_error['locations'] = [
                        {'line': loc.line, 'column': loc.column}
                        for loc in error.locations
                    ]

            return formatted_error

        if isinstance(error, GraphQLError):
            return format_graphql_error(error)

        return {'message': six.text_type(error)}

    def execute_graphql_request(self, *args, **kwargs):
        """
        Extract exceptions to send to sentry, because graphene will otherwise handle all exceptions by forwarding to api
        See: https://medium.com/@martin.samami/make-graphene-django-and-sentry-exceptions-work-together-f796be60a901
        """
        result = super().execute_graphql_request(*args, **kwargs)
        if result and result.errors:
            for error in result.errors:
                try:
                    raise error.original_error
                except Exception:
                    logger.exception("Failed to execute query")
        return result


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^graphql/?$', PkgGraphQLView.as_view(graphiql=True)),

]
