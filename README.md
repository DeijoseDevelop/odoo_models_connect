# odoo-models-connect

Odoo-Models-Connect is an library to improve interaction and communication with [Odoo](https://www.odoo.com/) XML-RPC [External API](https://www.odoo.com/documentation/15.0/webservices/odoo.html) for integration with other technologies.

## Installing

Install and update using [pip](https://pypi.org/project/odoo-models-connect/):

```
$ pip install odoo-models-connect
```

## Example

Initialize the required environment variables

1. Create an .env file
2. places the environment variables inside the file with these names:

   - DATABASE
   - USERNAME
   - PASSWORD
   - URL

For example .env:

    DATABASE='local_DB'
    USERNAME='admin@email.com'
    PASSWORD='123456'
    URL='http://localhost:8069'

3. import load_env_vars:

    ```
   from odoo_models_connect import load_env_vars
    ```

4. load environment variables:

   ```
   load_env_vars('path/to/environment')
   ```

   ##### NOTE: must end in .env

You can create a high-level interface by declaring models by extending models.OdooModel as follows:

```
from odoo_models_connect import models, fields, load_env_vars


load_env_vars(env_path='path/to/.env')


class ResUsers(models.OdooModel):
    _name = 'res.users'

    name = fields.StringField()
    login = fields.StringField()
    password = fields.StringField()
```

##### NOTE: it is necessary to load the environment variables before doing the inheritance of OdooModel

count of number of records:

```
>>> ResUsers.search_count()
4
```

search and read record by id:

```
>>> ResUsers.search_by_id(2)
<ResUsers id=2>
```

search and read records:

```
>>> ResUsers.search_read()
[<ResUsers id=2>, <ResUsers id=6>, <ResUsers id=7>, <ResUsers id=8>]
```

filter records:

```
>>> ResUsers.search_read(query=[["name", 'ilike', "John"]])
[<ResUsers id=2>, <ResUsers id=6>]
```

create a record:

```
user = ResUsers(
    name='John',
    login='John@mail.com',
    password='john123',
)

user.create()
```

update a record:

```
user = ResUsers(
    id=8,
    name='John2',
    login='John2@mail.com',
    password='john1234',
)

user.update()
```

delete a record:

```
user = ResUsers(id=10)

user.delete()
```

### Allowed data types:

- StringField
- BooleanField
- BinaryField
- DateField
- DateTimeField
- IntegerField
- FloatField
- MonetaryField
- Many2oneField
- Many2manyField
- One2manyField

##

## Other Features

Initialize the odoo connection:

```
from odoo_models_connect import ConnectOdoo

odoo = ConnectOdoo('http://localhost:8069', 'db_name')
```

User authentication in the odoo system:

```
uid = odoo.authenticate('user_email@mail.com', 'user_password')
```

In the case of wanting to make queries with the authenticated user in session it is necessary to use the reconnect method and pass a dictionary with the values of email, password and user id:

```
session = {
    "username": 'user_email@mail.com',
    "password": 'user_password',
    "uid": 7,
}

odoo.reconnect(session)
```

### Making queries

To make a simple search of all the elements of a model is used:

```
users = odoo.search_read('res.users')
```

You can place conditions or the fields you want to bring from each element:

```
users = odoo.search_read('res.users', condition=[['name', '=', 'Admin']], fields=['name', 'login', 'image_1920'])
```

The read() method works to do a search for elements with a list of element ids:

```
users = odoo.read('res.users', object_ids=[1, 7, 17])
```

You can also bring only the fields that are needed:

```
users = odoo.read('res.users', object_ids=[8, 25], fields=['name', 'login'])
```

#### NOTE: ids must be of type integer

You can fetch the id of all the elements of a model stored in a database:

```
users_ids = odoo.search_ids('res.users')
```

You can add a condition or domain:

```
users_ids = odoo.search_ids('res.users', domain=[
[('name', 'ilike', 'John%')]])
```

The create() method is used to create an element of a model in a database.

```
data = {
    "name": 'John',
    "login": 'John@mail.com',
    "password": 'john123'
}

odoo.create('res.users', data)
```

The update() method is used to update an element of a model in a database.

```
data = {
    "name": 'Juan',
    "login": 'Juan@mail.com',
    "password": 'Juan123'
}

user_id = 9

odoo.update('res.users', user_id, data)
```

The delete() method is used to delete an element of a model in a database.

```
user_id = 9

odoo.delete('res.users', user_id)
```
