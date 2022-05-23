import pdb
from pydoc import resolve

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
from rest_framework.test import APITestCase


class TestCaseSetup(APITestCase):
    def setUp(self) -> None:
        self.client = Client(enforce_csrf_checks=False)
        self.login = reverse("api:login")
        self.api_post = self.api_get_all = "/api/pdf/"
        self.api_get = self.api_patch = self.api_destroy = "/api/pdf/1/"

        self.userdata = {
            "username": "wrong",
            "email": "exe@ubuntu.com",
            "password": "#ubuntu@30",
        }

        res = User.objects.create_superuser(**self.userdata)
        res.is_staff = True
        res.save()

        return super().setUp()

    def create_data(self):

        file_test = SimpleUploadedFile(
            "Vishesh.pdf", b"filecontent", content_type="application/pdf"
        )

        data = {"pdfname": "ABC", "description": "-", "file": file_test}
        res = self.client.post(self.api_post, data=data, format="multipart")

        return res

    def tearDown(self) -> None:
        return super().tearDown()


class AccountTesting(TestCaseSetup):
    def test_user_can_login(self):
        res = self.client.post(
            self.login,
            data=self.userdata,
        )

        self.assertEqual(res.status_code, 200)

    def login_user(self):

        return self.client.post(self.login, data=self.userdata)


class PDFClassChecking(AccountTesting):
    def test_pdf_post_method(self):

        self.user = self.login_user()

        file_test = SimpleUploadedFile(
            "Vishesh.pdf", b"filecontent", content_type="application/pdf"
        )

        data = {"pdfname": "ABC", "description": "-", "file": file_test}
        res = self.client.post(self.api_post, data=data, format="multipart")

        self.assertEqual(res.status_code, 201)

    def test_pdf_get_all(self):

        res = self.client.get(self.api_get_all, format="json")

        self.assertEqual(res.status_code, 200)

    def test_pdf_get(self):

        res = self.client.get(self.api_get)

        self.assertEqual(res.status_code, 200)

    def test_pdf_patch(self):

        # Require To Login
        self.login_user()

        # Creating Data
        self.create_data()

        file_test = SimpleUploadedFile(
            "Vishesh.pdf", b"filecontent", content_type="application/pdf"
        )
        res = self.client.patch(
            self.api_patch,
            data={"pdfname": "ABCD", "description": "-"},
            content_type="application/json",
        )

        self.assertEqual(res.data["pdfname"], "ABCD")
        self.assertEqual(res.status_code, 204)

    def test_pdf_delete(self):

        self.login_user()

        self.create_data()

        res = self.client.delete(self.api_destroy)

        self.assertEqual(res.status_code, 204)
