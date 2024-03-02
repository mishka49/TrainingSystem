from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import ProductUsersGroups
from products.repositories import UserRepositories, ProductRepositories, LessonRepositories, \
    ProductUsersGroupsRepositories
from products.serializers import UserSerializer, ProductSerializer, LessonSerializer, GroupSerializer, \
    ProductUsersGroupsSerializer
from products.services import ProductGroupsCompoundService, ProductGroupsDistributionService, GroupService


class UserView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = UserRepositories.get_all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = ProductRepositories.get_all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            instance = ProductRepositories.get(request.data['id'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass


class LessonView(APIView):
    serializer_class = LessonSerializer

    def get(self, request):
        products = LessonRepositories.get_all()
        serializer = LessonSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass


class ProductUsersGroupsView(APIView):
    serializer_class = ProductUsersGroupsSerializer

    def get(self, request, product):
        products = ProductUsersGroupsRepositories.get_for_product(product)
        serializer = ProductUsersGroupsView.serializer_class(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProducts(APIView):
    serializer_class = ProductUsersGroupsSerializer

    def get(self, request, user):
        products = ProductUsersGroupsRepositories.get_for_user(user)
        serializer = UserProducts.serializer_class(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user):
        serializer = UserProducts.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupsCompoundView(APIView):
    serializer_class = ProductUsersGroupsSerializer

    def patch(self, request, product):
        users = ProductUsersGroupsRepositories.users_of_product(product)
        prod = ProductRepositories.get(product)

        new_compound = ProductGroupsCompoundService(
            min_members_in_group=prod.min_people_in_group,
            max_members_in_group=prod.max_people_in_group,
            number_of_users=len(users),
        )
        print(f"COMPOUND DISTRIBUTION {GroupService.create_groups(prod, new_compound.number_of_groups)}")

        distribution = ProductGroupsDistributionService.create_distribution(
            groups_compound=new_compound.groups_compound,
            users=users,
            groups=list(GroupService.create_groups(new_compound.number_of_groups))
        )

        result = ProductUsersGroupsRepositories.update_user_group(distribution)

        serializer = ProductUsersGroupsSerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
