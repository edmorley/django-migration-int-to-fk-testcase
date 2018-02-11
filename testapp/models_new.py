from django.db import models


class Foo(models.Model):
    pass


class Bar(models.Model):
    name = models.CharField(max_length=50)
    foo = models.ForeignKey(Foo, models.CASCADE, null=True)

    class Meta:
        unique_together = ('name', 'foo')
