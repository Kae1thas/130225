from django.test import TestCase
from django.urls import reverse

class PostDetailViewTest(TestCase):
    def setUp(self):
        self.posts = {
            1: {"id": 1, "title": "Первый пост", "text": "Текст первого поста"},
            2: {"id": 2, "title": "Второй пост", "text": "Текст второго поста"}
        }

    def test_post_detail(self):
        post_id = 1
        response = self.client.get(reverse("post_detail", args=[post_id]))
        self.assertEqual(response.status_code, 200)
        
        # Проверка, что объект есть в контексте
        self.assertIn("post", response.context, "Контекст страницы не содержит 'post'")
        
        post_from_context = response.context["post"]
        expected_post = self.posts[post_id]
        
        # Логирование для выявления различий
        print("EXPECTED:", expected_post)
        print("ACTUAL  :", post_from_context)
        
        # Проверка по ключам
        for key in expected_post:
            if key in post_from_context:
                if expected_post[key] != post_from_context[key]:
                    print(f"DIFFERENCE in {key}: Expected {expected_post[key]}, but got {post_from_context[key]}")
                self.assertEqual(expected_post[key], post_from_context[key], f"Значение ключа '{key}' не совпадает")
            else:
                self.fail(f"Ключ '{key}' отсутствует в контексте ответа")

        # Проверка текста без лишних пробелов и переносов строк
        self.assertEqual(expected_post["text"].strip(), post_from_context["text"].strip(), "Текст поста не совпадает после trim()")
