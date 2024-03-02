from copy import deepcopy

from products.models import User, Product, Lesson, ProductUsersGroups, Group


class UserRepositories:
    @staticmethod
    def get_all():
        return User.objects.all()

    @staticmethod
    def delete(user):
        return User.objects.get(id=user.id).delete()


class ProductRepositories:
    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get(product):
        return Product.objects.get(pk=product)

    @staticmethod
    def delete(product):
        return Product.objects.get(id=product.id).delete()


class LessonRepositories:
    @staticmethod
    def get_all():
        return Lesson.objects.all()

    @staticmethod
    def delete(lesson):
        return Lesson.objects.get(id=lesson.id).delete()


class ProductUsersGroupsRepositories:
    @staticmethod
    def get_for_product(product):
        return ProductUsersGroups.objects.select_related('user').filter(product=product)

    @staticmethod
    def get_for_user(user):
        return ProductUsersGroups.objects.filter(user=user)

    @staticmethod
    def users_of_product(product):
        return [item.user for item in ProductUsersGroups.objects.select_related('user').filter(product=product)]

    @staticmethod
    def update_user_group(product, users_group: dict):
        product_users_groups = ProductUsersGroups.objects.filter(product=product)

        for item in product_users_groups:
            item.group = users_group[item.user_id]

        return product_users_groups.save()


class GroupRepositories:
    @staticmethod
    def create_group(group):
        print(f"REPOS group: {group}")
        result = group.save()
        print(f"REPOS result: {result}")

        return result

