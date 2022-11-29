from django.db.models.functions import TruncDay
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.db.models import Q, Count, Sum, Avg
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from ...models import Category, Tag, Blog
from .serializers import CategorySerializer, TagSerializer, BlogSerializer


class CategoryListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/blog/v1/category-list/
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/blog/v1/tag-list/
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BlogListCreateView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/api/blog/v1/blog-list-create/
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super(BlogListCreateView, self).get_queryset().filter(is_active=True).order_by('-id')
        search = self.request.GET.get('q')

        search_condition = Q()
        if search:
            search_condition = (Q(title__icontains=search) | Q(content__icontains=search))
        qs = qs.filter(search_condition)
        return qs


class BlogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/api/blog/v1/blog-rud/<id>/
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]


class BlogStatistic(APIView):
    # http://127.0.0.1:8000/api/blog/v1/statistic/

    def get(self, *args, **kwargs):
        data = {}

        # ANNOTATE BY DAY
        queryset = Blog.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id'))
        for i in queryset:
            data[str(i.get('day').date())] = i.get('count')
        return Response(data)

        # AGGREGATE
        # total = Blog.objects.aggregate(sum=Sum('price'))
        # avg = Blog.objects.aggregate(sum=Avg('price'))
        # data['total'] = total
        # data['avg'] = avg
        # return Response(data)
        #
