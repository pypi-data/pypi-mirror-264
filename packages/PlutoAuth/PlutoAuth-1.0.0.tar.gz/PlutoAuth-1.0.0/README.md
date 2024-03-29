
# PlutoAuth

PlutoAuth is a Python SDK for interacting with the Pluto Authentication API. It provides a simple and pythonic way to use the API's functionality.

This library was made by the Official **Pluto Authentication Team**.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PlutoAuth.

```bash
pip install PlutoAuth
```
or
```bash
python3 -m pip install PlutoAuth
```

## Example Usage

```python
from PlutoAuth import PlutoAPI

db_uuid = "DBUUID - Get from dashboard"
db_user = {"username": "username", "password": "password"}

# Read database/userbase
api = PlutoAPI(db_uuid, db_user)
print(api.read_database()) # Should return the database as JSON

# Get the user who is currently signed in on the web
me = api.me(db_user.get('username'), db_user.get('password'))
print(me) # Should return the user object
print("Credits: " + me.credits)
```

## API Methods

The `PlutoAPI` class provides the following methods:

- `me(username: str, password: str)`: Get the user who is currently signed in on the web.
- `read_database()`: Read database/userbase.
- `add_db_user(new_user, permissions)`: Add a new access user to the database.
- `remove_db_user(username)`: Remove a DB user from the database.
- `update_db_user_permissions(username, permissions)`: Update a DB user's permissions.
- `add_userbase_user(new_user, extra_fields=None)`: Add a new auth user to the database.
- `remove_userbase_user(username)`: Remove an auth user from the database.
- `update_userbase_user(update_user)`: Update an auth user's extra fields.
- `authenticate_user(auth_user)`: Check the credentials of an auth user.

For more details on these methods and the data they require, refer to the [Pluto API documentation](https://pluto-mc.net/documentation). (Must be signed in to view)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)