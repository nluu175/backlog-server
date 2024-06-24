from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from ..models.Backlog import Backlog
from ..serializers import BacklogSerializer


class BacklogView(APIView):
    http_method_names = ["get"]

    def get(self, request, backlog_id):
        backlog = get_object_or_404(Backlog, id=backlog_id)
        serializer = BacklogSerializer(backlog)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BacklogsView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request):
        backlogs = Backlog.objects.all()
        serializer = BacklogSerializer(backlogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
