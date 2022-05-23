import requests
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import PDFModel
from .serializations import PDFSerializer


class PDFView(ViewSet):

    queryset = PDFModel.objects.all()
    serializer_class = PDFSerializer

    def list(self, request):
        serialize = self.serializer_class(
            self.queryset, many=True, context={"request": request}
        )

        return Response(serialize.data)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "pdfname": {"type": "string"},
                    "description": {"type": "string"},
                    "file": {"type": "string", "format": "binary"},
                },
            }
        },
        responses=PDFSerializer,
    )
    def create(self, request):

        serialize = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serialize.is_valid():
            serialize.save()

            return Response(serialize.data, status=status.HTTP_201_CREATED)

        return Response(serialize.errors)

    def retrieve(self, request, pk=None):
        # Check wether pk is valid or not valid
        try:
            query = PDFModel.objects.get(pk=pk)
        except Exception:
            data = {"message": "Not Found"}

            return Response(data)

        serialize = self.serializer_class(query, context={"request": request})
        print(type(serialize.data))
        return Response(serialize.data)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "pdfname": {"type": "string"},
                    "description": {"type": "string"},
                    "file": {"type": "string", "format": "binary"},
                },
            }
        },
        responses=PDFSerializer,
    )

    ## This is patch request
    def partial_update(self, request, pk=None):

        # Getting Query in data
        try:
            query = PDFModel.objects.get(pk=pk)
        except Exception:
            data = {"message": "Not Found"}
            return Response(data)

        serialize = self.serializer_class(
            query, data=request.data, partial=True, context={"request": request}
        )

        if serialize.is_valid():
            serialize.save()

            return Response(serialize.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serialize.errors)

    # Delete Test in Unix

    def destroy(self, request, pk=None):
        ## For Debug purpose not for production ready
        # Getting Query in data
        try:
            query = PDFModel.objects.get(pk=pk)
        except Exception:
            data = {"message": "Not Found"}
            return Response(data)

        file_name = query.file.name
        query.file.delete()
        query.delete()

        data = {"file_name": file_name, "message": "File successfully deleted."}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):

        if self.action in ("list", "retrieve"):
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]


class UserLogin(APIView):
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string", "format": "password"},
                },
            }
        }
    )
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            session_id = request.session._session_key
            data = {
                "username": user.username,
                "message": "Login Done",
                "session": session_id,
            }

            return Response(data)

        data = {"message": "User Not Found"}

        return Response(data=data)
