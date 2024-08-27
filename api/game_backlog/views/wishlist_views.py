from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models.Wishlist import Wishlist

from ..serializers.wishlist_serializer import WishlistSerializer
from ..custom.pagination import WishlistPagination


# api/wishlists/{wishlist_id}
class WishlistView(APIView):
    http_method_names = ["get", "put"]

    def get(self, request, wishlist_id):
        backlog = get_object_or_404(Wishlist, id=wishlist_id)
        serializer = WishlistSerializer(backlog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, wishlist_id):
        wishlist = get_object_or_404(Wishlist, id=wishlist_id)
        serializer = WishlistSerializer(wishlist, data=request.data)

        if serializer.is_valid():
            order = serializer.validated_data["order"]

            wishlist.order = order

            return Response(
                WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/wishlists
class WishlistsView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        wishlists = Wishlist.objects.select_related("game").all()

        # Check for pagination parameters
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        if page or page_size:
            paginator = WishlistPagination()
            paginated_wishlists = paginator.paginate_queryset(wishlists, request)
            serializer = WishlistSerializer(paginated_wishlists, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = WishlistSerializer(wishlists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            game = serializer.validated_data["game"]
            order = serializer.validated_data["order"]

            wishlist = Wishlist.objects.create(user=user, game=game, order=order)

            return Response(
                WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
