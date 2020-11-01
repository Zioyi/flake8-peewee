flake8-peewee
=============
flake8 plugin which checks for peewee syntax error.

for example:
```python
# User is peewee.Model
# we want to query all users who are younger than 20 years old

# this is correct usage:
users = User.select().where(User.age < 20)

# but we may carelessly write the following form：
users = User.select(User.age < 20)

# it will be catastrophic
```

so I want to use flake plugin mechanism help us check.

## flake8 codes

| Code   | Description                                            |
|--------|--------------------------------------------------------|
| PWE101 | `select()` inner comparison expression are not allowed |
