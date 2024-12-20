from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse

# Create your tests here.

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        la funcion was_published_recently() debe retornar falso para
        las preguntas en futuro
        """
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        
        self.assertIs(future_question.was_published_recently(), False)
        
    
    def test_was_published_recently_with_old_question(self):
        """was_published_recently() devuelve Falso para las preguntas cuya fecha de publicación sea anterior a 1 día.
        """
        
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)
    
    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() devuelve True para las preguntas cuya fecha de publicación esté dentro del último día
        """
        
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),True)
        
        
        
def create_question(question_text, days):
        
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)
    

class QuestionIndexViewTests(TestCase):
    
    def test_no_question(self):
        """Si no existen preguntas, se muestra un mensaje apropiado."""
        response =self.client.get(reverse("polls:hello"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"],[])
        
    def test_part_question(self):
        """Las preguntas con una fecha de publicación en el pasado se muestran en la
            página de índice. """
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:hello'))
        self.assertQuerySetEqual(response.context['latest_question_list'],[question])
        
    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed onthe index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:hello"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:hello"))
        self.assertQuerySetEqual(
        response.context["latest_question_list"],
        [question],
        )
        
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:hello"))
        self.assertQuerySetEqual(
        response.context["latest_question_list"],
        [question2, question1],
        )    