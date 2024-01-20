from django.urls import path, include

from .views import ContentListAPIView

app_name = 'content'
urlpatterns = [
    path('contents/', include(([
        path('', ContentListAPIView.as_view({
            'get': 'list'
        })),
        path('<int:pk>/rating/', ContentListAPIView.as_view({
            'post': 'rating'
        })),
    ]))),
]