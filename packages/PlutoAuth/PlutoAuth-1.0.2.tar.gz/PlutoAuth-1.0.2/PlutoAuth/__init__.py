import requests
from pydantic import BaseModel

class PlutoRequestFailedError(Exception):
    pass
class PlutoRequestFailedWarning(Warning):
    pass

class PlutoUserLoginError(Exception):
    pass

class PlutoUser(BaseModel):
    username: str
    databases: dict
    credit: float

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return self.username
    
    def __getitem__(self, key):
        return self.databases[key]
    
    def __setitem__(self, key, value):
        self.databases[key] = value

    def __delitem__(self, key):
        del self.databases[key]

    def __iter__(self):
        return iter(self.databases)
    
    def __len__(self):
        return len(self.databases)
    
    def __contains__(self, key):
        return key in self.databases

class PlutoAPI:
    def __init__(self, db_uuid: str, db_user: dict):
        '''Official API Wrapper for Pluto Authentication
        @param db_uuid: The UUID of the database - Can be found on the Pluto dashboard
        @param db_user: The user object of the user who has access to the database
            > Example: {"username": "admin", "password": "password123"}
        
        Example program:
        ```python
        from PlutoAuth import PlutoAPI

        db_uuid = "DATABASE UUID HERE"
        db_user = {"username": "USERNAME HERE", "password": "PASS HERE"}

        # Read database/userbase
        api = PlutoAPI(db_uuid, db_user)
        print(api.read_database()) # Should return the database as JSON
        ```

        Methods:
        - me: Get the user who is currently signed in on the web
            - Requires your login details (To get your Bearer token)
            - Useful for checking credits, getting DB UUIDs, etc.
            - Returns in a PlutoUser object

        - read_database: Read database/userbase
        - add_db_user: Add a new access user to the database (dbuser who can access the database)
        - update_db_user_permissions: Update a DB user's permissions (dbuser who can access the database)
        - remove_db_user: Remove a DB user from the database (dbuser who can access the database)
        - add_userbase_user: Add a new auth user to the database (Authentication service user)
        - remove_userbase_user: Remove an auth user from the database (Authentication service user)
        - update_userbase_user: Update an auth user's extra fields (Authentication service user)
        - authenticate_user: Check the credentials of an auth user

        For the data required for each of these methods, refer to the Pluto API documentation
            > https://pluto-mc.net/documentation (Must be signed in to view)
        '''
        self.base_url = "https://pluto-mc.net/"
        self.db_uuid = db_uuid
        self.db_user = db_user

    def _send_request(self, method, endpoint, data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        if method == "GET":
            response = requests.get(url, json=data, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, json=data, headers=headers)
        else:
            raise ValueError(f"Invalid method {method}")

        if response.status_code != 200 and response.status_code != 201:
            raise PlutoRequestFailedError(f"Request failed with status {response.status_code}")
        
        return response.json()
    
    def me(self, username: str, password: str):
        '''Get the user who is currently signed in on the web
            > Requires your login details (To get your Bearer token)
            > Useful for checking credits, getting DB UUIDs, etc.
        '''
        token = self._send_request("POST", "login", data={"username": username, "password": password})

        # fastify.get('/users/me', async (request, reply) => {
        #     const db = get_db();
        #     const token = request.headers.authorization;
        #     ...
        access_token = token.get("access_token")
        user = self._send_request("GET", "users/me", headers={"Authorization": f"Bearer {access_token}"})
        
        try: return PlutoUser(**user)
        except TypeError: return user; print('[WARN] PlutoUser object could not be created, returning JSON instead')

    def read_database(self):
        '''Read database/userbase'''
        return self._send_request("POST", f"databases/{self.db_uuid}", {"user": self.db_user})

    def add_db_user(self, new_user, permissions):
        '''Add a new access user to the database (dbuser who can access the database)'''
        data = {"user": self.db_user, "new_user": new_user, "permissions": permissions}
        return self._send_request("POST", f"databases/{self.db_uuid}/users/db", data)

    def remove_db_user(self, username):
        '''Remove a DB user from the database (dbuser who can access the database)'''
        data = {"user": self.db_user, "username": username}
        return self._send_request("DELETE", f"databases/{self.db_uuid}/users/db", data)

    def update_db_user_permissions(self, username, permissions):
        '''Update a DB user's permissions (dbuser who can access the database)'''
        data = {"user": self.db_user, "username": username, "permissions": permissions}
        return self._send_request("PUT", f"databases/{self.db_uuid}/users/db", data)

    def add_userbase_user(self, new_user, extra_fields=None):
        '''Add a new auth user to the database (Authentication service user)'''
        data = {"user": self.db_user, "new_user": new_user, "extra_fields": extra_fields or {}}
        return self._send_request("POST", f"databases/{self.db_uuid}/users/auth", data)

    def remove_userbase_user(self, username):
        '''Remove an auth user from the database (Authentication service user)'''
        data = {"user": self.db_user, "username": username}
        return self._send_request("DELETE", f"databases/{self.db_uuid}/users/auth", data)

    def update_userbase_user(self, update_user):
        '''Update an auth user's extra fields (Authentication service user)'''
        data = {"user": self.db_user, "update_user": update_user}
        return self._send_request("PUT", f"databases/{self.db_uuid}/users/auth", data)

    def authenticate_user(self, auth_user):
        '''Check the credentials of an auth user'''
        data = {"user": self.db_user, "username": auth_user["username"], "password": auth_user["password"]}
        return self._send_request("POST", f"databases/{self.db_uuid}/users/authenticate", data)
    
    def __str__(self):
        return f"Pluto API for {self.db_uuid}"
    
    def __repr__(self):
        return f"Pluto API for {self.db_uuid}"

if __name__ == "__main__":
    raise Exception("This is a library and should not be executed directly!")