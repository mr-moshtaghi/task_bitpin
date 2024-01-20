from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Content, Rating
from .serializers import ContentSerializer, RatingSerializer


class ContentListAPIView(viewsets.ViewSet):

    def list(self, request):
        context = {
            'user': request.user
        }
        queryset = Content.objects.all()
        serializer = ContentSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def rating(self, request, pk, *args, **kwargs):
        content = Content.objects.filter(pk=pk).first()
        if not content:
            return Response(
                {'Bad Request': "Your request is not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Rating.objects.update_or_create(
            user=request.user,
            content_id=pk,
            defaults={
                "rating": serializer.validated_data["rating"]
            }
        )
        return Response(ContentSerializer(content, context={'user': request.user}).data)
