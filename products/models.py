from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    author = models.OneToOneField('User', on_delete=models.SET_NULL, null=True)
    min_people_in_group = models.IntegerField()
    max_people_in_group = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    coast = models.FloatField(null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)


class Lesson(models.Model):
    name = models.CharField(max_length=150, null=True)
    video_ref = models.CharField(max_length=200, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)


class Group(models.Model):
    name = models.CharField(max_length=100, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)


class ProductUsersGroups(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey('Group', on_delete= models.SET_NULL, null=True)

