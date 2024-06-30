from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from ..models.Backlog import Backlog
from ..serializers import BacklogSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100


class BacklogView(APIView):
    http_method_names = ["get", "put"]

    def get(self, request, backlog_id):
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, backlog_id):
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog, data=request.data)

        if serializer.is_valid():
            # TODO: make fields optional
            # user = serializer.validated_data["user"]
            # game = serializer.validated_data["game"]
            backlog_status = serializer.validated_data["status"]
            rating = serializer.validated_data["rating"]
            comment = serializer.validated_data["comment"]
            playtime = serializer.validated_data["playtime"]

            # update status
            backlog.status = backlog_status
            backlog.rating = rating
            backlog.comment = comment
            backlog.playtime = playtime

            backlog.save()

            return Response(
                BacklogSerializer(backlog).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BacklogsView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        # backlogs = Backlog.objects.all()
        # serializer = BacklogSerializer(backlogs, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        # Step 2: Instantiate the paginator and get the paginated queryset
        paginator = CustomPagination()
        backlogs = Backlog.objects.all()
        paginated_backlogs = paginator.paginate_queryset(backlogs, request)
        
        # Step 3: Serialize the paginated queryset
        serializer = BacklogSerializer(paginated_backlogs, many=True)
        
        # Step 4: Return the paginated response
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = BacklogSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            game = serializer.validated_data["game"]
            # cannot name this one status because this one will override status in rest_framework
            progress_status = serializer.validated_data["status"]
            rating = serializer.validated_data["rating"]
            comment = serializer.validated_data["comment"]
            playtime = serializer.validated_data["playtime"]

            backlog = Backlog.objects.create(
                user=user,
                game=game,
                status=progress_status,
                rating=rating,
                comment=comment,
                playtime=playtime,
            )

            return Response(
                BacklogSerializer(backlog).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
