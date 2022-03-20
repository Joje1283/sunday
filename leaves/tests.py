from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Use, Grant, Type

User = get_user_model()


class LeaveTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.일반사용자1 = User.objects.create(username="일반사용자1")
        self.일반사용자2 = User.objects.create(username="일반사용자2")
        self.일반사용자3 = User.objects.create(username="일반사용자3")
        self.일반사용자4 = User.objects.create(username="일반사용자4")
        self.일반사용자5 = User.objects.create(username="일반사용자5")
        self.관리자 = User.objects.create(username="재무팀사용자")
        self.관리자.is_staff = True
        self.관리자.save()

    def test_관리자가_일반사용자에게_휴가를_부여한다(self):
        self.client.force_login(self.관리자)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자1.pk}/leaves/grant/",
            data={"type": Type.ANNURE, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자1.pk}/leaves/grant/",
            data={"type": Type.SPECIAL, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자2.pk}/leaves/grant/",
            data={"type": Type.ANNURE, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자3.pk}/leaves/grant/",
            data={"type": Type.ANNURE, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자4.pk}/leaves/grant/",
            data={"type": Type.ANNURE, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자5.pk}/leaves/grant/",
            data={"type": Type.ANNURE, "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Grant.objects.count(), 6)

    def test_일반사용자가_휴가를_사용한다(self):
        self.client.force_login(self.일반사용자1)

        res = self.client.post(
            path="/leaves/use/",
            data={
                "type": Type.ANNURE,
                "start_date": "2022-01-02",
                "end_date": "2022-01-01",
                "start_date_time": "11:00:00"
            }
        )
        self.assertEqual(res.status_code, 400)

        res = self.client.post(
            path="/leaves/use/",
            data={
                "type": Type.ANNURE,
                "start_date": "2022-01-02",
                "end_date": "2022-01-03",
                "start_date_time": "11:00:00"
            }
        )
        self.assertEqual(res.status_code, 201)

    def test_일반사용자가_남은_휴가를_조회한다(self):
        pass

    def test_일반사용자가_올해_휴가_내역을_조회한다(self):
        pass

    def test_일반사용자가_예약된_휴가를_조회한다(self):
        pass

    def test_관리자가_모든_예약된_휴가를_조회한다(self):
        pass
