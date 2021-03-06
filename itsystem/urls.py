from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ContributorViewSet, ProjectViewSet, IssueViewSet, CommentViewSet, SignUpView, LoginView

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'users', ContributorViewSet, basename='contributors')
projects_router.register(r'issues', IssueViewSet, basename='issues')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issues')
issues_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
	path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),
    path(r'', include(router.urls)),
    path(r'', include(projects_router.urls)),
    path(r'', include(issues_router.urls)),
]