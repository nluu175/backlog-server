from typing import Any, Dict, Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

from ..models.Wishlist import Wishlist
from ..serializers.wishlist_serializer import WishlistSerializer
from ..custom.pagination import WishlistPagination


class WishlistView(APIView):
    """
    API View for handling single wishlist operations.
    Endpoint: /api/wishlists/{wishlist_id}
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def _update_wishlist(
        self, wishlist: Wishlist, validated_data: Dict[str, Any]
    ) -> Wishlist:
        """
        Update wishlist with validated data.

        Args:
            wishlist: Wishlist instance to update
            validated_data: Validated data from serializer

        Returns:
            Updated Wishlist instance
        """
        wishlist.order = validated_data["order"]
        wishlist.save()
        return wishlist

    @transaction.atomic
    def get(self, request: HttpRequest, wishlist_id: str) -> Response:
        """
        Retrieve a specific wishlist entry.

        Args:
            request: HTTP request object
            wishlist_id: UUID of the wishlist entry

        Returns:
            Response containing the serialized wishlist data
        """
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request: HttpRequest, wishlist_id: str) -> Response:
        """
        Update a specific wishlist entry.

        Args:
            request: HTTP request object with updated wishlist data
            wishlist_id: UUID of the wishlist entry

        Returns:
            Response containing the updated wishlist data or error message
        """
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        serializer = WishlistSerializer(wishlist, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_wishlist = self._update_wishlist(wishlist, serializer.validated_data)
        return Response(
            WishlistSerializer(updated_wishlist).data, status=status.HTTP_201_CREATED
        )


class WishlistsView(APIView):
    """
    API View for handling multiple wishlist operations.
    Endpoint: /api/wishlists
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def _handle_pagination(
        self,
        queryset: Any,
        request: HttpRequest,
        page: Optional[str],
        page_size: Optional[str],
    ) -> Response:
        """
        Handle pagination of wishlist queryset if pagination parameters are provided.

        Args:
            queryset: The queryset to paginate
            request: HTTP request object
            page: Page number
            page_size: Number of items per page

        Returns:
            Response with either paginated or full results
        """
        if page or page_size:
            paginator = WishlistPagination()
            paginated_wishlists = paginator.paginate_queryset(queryset, request)
            serializer = WishlistSerializer(paginated_wishlists, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = WishlistSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _create_wishlist(self, validated_data: Dict[str, Any]) -> Wishlist:
        """
        Create a new wishlist entry from validated data.

        Args:
            validated_data: Validated data from serializer

        Returns:
            Newly created Wishlist instance
        """
        return Wishlist.objects.create(
            user=validated_data["user"],
            game=validated_data["game"],
            order=validated_data["order"],
        )

    @transaction.atomic
    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve all wishlist entries with optional pagination.

        Args:
            request: HTTP request object with optional page and size query parameters

        Returns:
            Response containing the serialized wishlist data
        """
        wishlists = Wishlist.objects.select_related("game").all()
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        return self._handle_pagination(wishlists, request, page, page_size)

    @transaction.atomic
    def post(self, request: HttpRequest) -> Response:
        """
        Create a new wishlist entry.

        Args:
            request: HTTP request object containing wishlist data

        Returns:
            Response with created wishlist data or validation errors
        """
        serializer = WishlistSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        wishlist = self._create_wishlist(serializer.validated_data)
        return Response(
            WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED
        )
