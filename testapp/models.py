from django.db import models


class Foo(models.Model):
    pass


class Bar(models.Model):
    name = models.CharField(max_length=50)
    foo_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name', 'foo_id')
