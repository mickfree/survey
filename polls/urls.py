from django.urls import path
from .views import *

app_name = 'polls'

urlpatterns = [
        path('', IndexView.as_view() , name = 'hello'),
        # ex: /polls/5/
        path('<int:question_id>/detail/', detail, name='detail'),
        path('<int:question_id>/results/', results, name='results'),
        path('<int:question_id>/votes/', vote, name='vote'),
]
