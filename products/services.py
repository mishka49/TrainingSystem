import math

from products.models import Group
from products.repositories import GroupRepositories


# from products.repositories import ProductUsersGroupsRepositories


class ProductGroupsCompoundService:
    def __init__(self, min_members_in_group, max_members_in_group, number_of_users: int):
        self.min_members_in_group = min_members_in_group
        self.max_members_in_group = max_members_in_group
        self.number_of_users = number_of_users
        self.number_of_groups = self.determine_number_of_group()
        self.groups_compound = self.determine_groups_compound()

    def determine_groups_compound(self):
        min_members_in_group = int(self.number_of_users / self.number_of_groups)
        print(min_members_in_group)

        compound = [min_members_in_group for _ in range(self.number_of_groups)]

        iter = 0
        print(f'While:{self.number_of_users - min_members_in_group * self.number_of_groups}')
        print(f'Number group: {self.number_of_groups}')
        while iter < (self.number_of_users - min_members_in_group * self.number_of_groups):
            compound[iter] += 1
            iter += 1

        return compound

    def determine_number_of_group(self):
        return math.ceil(self.number_of_users / self.max_members_in_group)


class ProductGroupsDistributionService:
    @staticmethod
    def create_distribution(groups_compound, users, groups):
        distribution = list()
        count_in_group = 0
        group = 0

        for user in users:
            if count_in_group >= groups_compound[group]:
                group += 1
                count_in_group = 0

            distribution[user] = groups[group]
            count_in_group += 1

        return distribution

class GroupService:
    @staticmethod
    def create_groups(product, number_of_groups):
        groups = list()
        for _ in range(number_of_groups):
            res = GroupRepositories.create_group(Group(product=product))
            print(res)
            groups.append(res)

        return groups



