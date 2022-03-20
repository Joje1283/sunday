from django.contrib.auth import get_user_model
from django.test import TestCase


class LeaveTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        # User
        User = get_user_model()
        self.일반사용자 = User.objects.create(username="일반사용자")
        self.관리자 = User.objects.create(username="재무팀사용자")
        self.관리자.is_staff = True
        self.관리자.save()

    def test_휴가를_부여한다(self):
        self.client.force_login(self.관리자)
        res = self.client.post(
            path=f"/accounts/{self.일반사용자.pk}/leaves/grant/",
            data={"type": "A", "days": 15},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)

    def test_휴가를_사용한다(self):
        self.client.force_login(self.일반사용자)
        res = self.client.post(
            path="/leaves/use/",
            data={
                "type": "A",
                "start_date": "2022-01-02",
                "end_date": "2022-01-03",
                "start_date_time": "11:00:00"
            }
        )
        self.assertEqual(res.status_code, 201)
