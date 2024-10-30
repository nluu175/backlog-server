from typing import Any, Dict, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

from ..models.Backlog import Backlog
from ..models.User import User
from ..serializers.backlog_serializer import BacklogSerializer
from ..custom.pagination import BacklogPagination


class BacklogView(APIView):
    """
    API View for handling single backlog operations.
    Endpoint: /api/backlogs/{backlog_id}
    """

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def get(self, request: HttpRequest, backlog_id: str) -> Response:
        """
        Retrieve a specific backlog entry.

        Args:
            request: HTTP request object
            backlog_id: UUID of the backlog entry

        Returns:
            Response containing the serialized backlog data
        """
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request: HttpRequest, backlog_id: str) -> Response:
        """
        Update a specific backlog entry.

        Args:
            request: HTTP request object with updated backlog data
            backlog_id: UUID of the backlog entry

        Returns:
            Response containing the updated backlog data or error message
        """
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for attr, value in serializer.validated_data.items():
            setattr(backlog, attr, value)
        backlog.save()

        return Response(BacklogSerializer(backlog).data, status=status.HTTP_201_CREATED)


class BacklogsView(APIView):
    """
    API View for handling multiple backlog operations.
    Endpoint: /api/backlogs
    """

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def _handle_pagination(
        self,
        queryset: Any,
        request: HttpRequest,
        page: Optional[str],
        page_size: Optional[str],
    ) -> Response:
        """
        Handle pagination of backlog queryset if pagination parameters are provided.

        Args:
            queryset: The queryset to paginate
            request: HTTP request object
            page: Page number
            page_size: Number of items per page

        Returns:
            Response with either paginated or full results
        """
        if page or page_size:
            paginator = BacklogPagination()
            paginated_backlogs = paginator.paginate_queryset(queryset, request)
            serializer = BacklogSerializer(paginated_backlogs, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = BacklogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve all backlog entries with optional pagination, sorted by game name.

        Args:
            request: HTTP request object with optional page and size query parameters

        Returns:
            Response containing the serialized backlog data, sorted by game name
        """
        backlogs = Backlog.objects.select_related("game").all().order_by("game__name")
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        return self._handle_pagination(backlogs, request, page, page_size)

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Create a new backlog entry.

        Args:
            request: HTTP request object containing backlog data

        Returns:
            Response with created backlog data or validation errors
        """
        serializer = BacklogSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        backlog = Backlog.objects.create(**serializer.validated_data)
        return Response(BacklogSerializer(backlog).data, status=status.HTTP_201_CREATED)


class BacklogsByUserView(APIView):
    """
    API View for handling multiple backlog operations filtered by User ID.
    Endpoint: /api/backlogs
    """

    http_method_names = ["get"]

    def _handle_pagination(
        self,
        queryset: Any,
        request: HttpRequest,
        page: Optional[str],
        page_size: Optional[str],
    ) -> Response:
        """
        Handle pagination of backlog queryset if pagination parameters are provided.

        Args:
            queryset: The queryset to paginate
            request: HTTP request object
            page: Page number
            page_size: Number of items per page

        Returns:
            Response with either paginated or full results
        """
        if page or page_size:
            paginator = BacklogPagination()
            paginated_backlogs = paginator.paginate_queryset(queryset, request)
            serializer = BacklogSerializer(paginated_backlogs, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = BacklogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest, user_id: str) -> Response:
        """
        Retrieve all backlog entries for a specific user, sorted by game name.

        Args:
            request: HTTP request object with optional page and size query parameters
            user_id: UUID of the user whose backlogs to retrieve

        Returns:
            Response containing the serialized backlog data for the specified user
        """

        get_object_or_404(User, id=user_id)

        backlogs = (
            Backlog.objects.select_related("game")
            .filter(user_id=user_id)
            .order_by("game__name")
        )
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        return self._handle_pagination(backlogs, request, page, page_size)
