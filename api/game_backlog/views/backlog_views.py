from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpRequest

from ..models.Backlog import Backlog
from ..serializers.backlog_serializer import BacklogSerializer
from ..custom.pagination import BacklogPagination


# api/backlogs/{backlog_id}
class BacklogView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "put"]

    def get(self, request: HttpRequest, backlog_id):
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request: HttpRequest, backlog_id):
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog, data=request.data)

        if serializer.is_valid():
            # # TODO: make fields optional
            # # user = serializer.validated_data["user"]
            # # game = serializer.validated_data["game"]
            # backlog_status = serializer.validated_data["status"]
            # rating = serializer.validated_data["rating"]
            # comment = serializer.validated_data["comment"]
            # playtime = serializer.validated_data["playtime"]
            # favourite = serializer.validated_data["favourite"]

            # # update status
            # backlog.status = backlog_status
            # backlog.rating = rating
            # backlog.comment = comment
            # backlog.playtime = playtime
            # backlog.favourite = favourite

            # backlog.save()

            backlog.update(**serializer.validated_data)

            return Response(
                BacklogSerializer(backlog).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/backlogs
class BacklogsView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    http_method_names = ["get", "post"]

    def get(self, request: HttpRequest):
        backlogs = Backlog.objects.select_related("game").all()

        # Check for pagination parameters
        page = request.query_params.get("page")
        page_size = request.query_params.get("size")

        if page or page_size:
            # If pagination parameters are provided, paginate the queryset
            paginator = BacklogPagination()
            paginated_backlogs = paginator.paginate_queryset(backlogs, request)
            serializer = BacklogSerializer(paginated_backlogs, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            # If no pagination parameters, return all results
            serializer = BacklogSerializer(backlogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: HttpRequest):
        serializer = BacklogSerializer(data=request.data)

        if serializer.is_valid():
            # user = serializer.validated_data["user"]
            # game = serializer.validated_data["game"]
            # # cannot name this one status because this one will override status in rest_framework
            # progress_status = serializer.validated_data["status"]
            # rating = serializer.validated_data["rating"]
            # comment = serializer.validated_data["comment"]
            # playtime = serializer.validated_data["playtime"]
            # favourite = serializer.validated_data["favourite"]

            # backlog = Backlog.objects.create(
            #     user=user,
            #     game=game,
            #     status=progress_status,
            #     rating=rating,
            #     comment=comment,
            #     playtime=playtime,
            #     favourite=favourite,
            # )

            backlog = Backlog.objects.create(**serializer.validated_data)

            serializer = BacklogSerializer(backlog).data

            return Response(serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
