from django.urls import path, include
from .views import UserView, ProjectView, IssueView, CommentView, SignUpView, LoginView


urlpatterns = [
	path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('projects/', ProjectView.as_view()),
    path('projects/<project_id>', ProjectView.as_view()),
    path('projects/<project_id>/users/', UserView.as_view()),
    path('projects/<project_id>/users/<user_id>', UserView.as_view()),
    path('projects/<project_id>/issues/', IssueView.as_view()),
    path('projects/<project_id>/issues/<issue_id>', IssueView.as_view()),
    path('projects/<project_id>/issues/<issue_id>/comments/', CommentView.as_view()),
    path('projects/<project_id>/issues/<issue_id>/comments/<comment_id>', CommentView.as_view()),
]