## STR:

1. Clone this repo
2. `pip install https://github.com/django/django/archive/master.zip`
3. `./manage.py migrate`
4. `cp testapp/models_new.py testapp/models.py`
5. `./manage.py makemigrations --name broken_migration`
6. `./manage.py migrate`

## Expected:

New migration is created/applied successfully.

## Actual:

The new `0002_broken_migration.py` migration incorrectly lists the `AddField`
operation before the `RemoveField` operation...

```py
    operations = [
        migrations.AddField(
            model_name='bar',
            name='foo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='testapp.Foo'),
        ),
        migrations.RemoveField(
            model_name='bar',
            name='foo_id',
        ),
        migrations.AlterUniqueTogether(
            name='bar',
            unique_together={('name', 'foo')},
        ),
    ]
```

Which results in an exception at step 6...

```
$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, testapp
Running migrations:
  Applying testapp.0002_broken_migration...Traceback (most recent call last):
  File "/c/Users/Ed/.virtualenvs/django-master/lib/python3.6/site-packages/django/db/backends/utils.py", line 83, in _execute
    return self.cursor.execute(sql)
  File "/c/Users/Ed/.virtualenvs/django-master/lib/python3.6/site-packages/django/db/backends/sqlite3/base.py", line 290, in execute
    return Database.Cursor.execute(self, query)
sqlite3.OperationalError: duplicate column name: foo_id
```

## Additional notes:
* This affects both the SQLite backend and the MySQL backend (others not tested).
* Without the `unique_together` on model `Bar`, the bug does not occur.
* At time of testing, django master was at revision `6d794fb76212bb8a62fe2cd97cff173054e1c626`.
* This also affects Django 1.11.10.
