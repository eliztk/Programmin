import hashlib
from datetime import datetime

class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self._hash_password(password) == self.password_hash

    def __str__(self):
        return f"{self.__class__.__name__}({self.username})"

class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password, is_active=True)
        self.permissions = permissions if permissions is not None else []

    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)

    def has_permission(self, permission):
        return permission in self.permissions

    def __str__(self):
        return f"Administrator: {self.username}, дозволи: {', '.join(self.permissions)}"

class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_login = None

    def update_login_time(self):
        self.last_login = datetime.now()

    def __str__(self):
        login_time = self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else "Ніколи"
        return f"RegularUser: {self.username}, останній вхід: {login_time}"

class GuestUser(User):
    def __init__(self, username="guest"):
        super().__init__(username, password="", is_active=False)
        self.restricted_access = True

    def get_guest_notice(self):
        return "Ви маєте обмежений доступ до системи."

class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user, by_admin=None):
        if by_admin:
            if not isinstance(by_admin, Administrator):
                print("Лише адміністратор має можливість додавати користувачів.")
                return
            if not by_admin.has_permission("manage_users"):
                print("Ви не маєте дозволу на додавання користувачів.")
                return

        if user.username in self.users:
            print(f"Користувач '{user.username}' вже існує.")
        else:
            self.users[user.username] = user
            print(f"Користувача '{user.username}' успішно додано.")

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            if isinstance(user, RegularUser):
                user.update_login_time()
            return user
        return None

admin = Administrator("Admin", "Mg0G23", ["manage_users"])
print(admin.has_permission("manage_users"))  # True

user = RegularUser("R1ta67", "Gen20tn")
user.update_login_time()
print(user.last_login)

guest = GuestUser()
print(guest.get_guest_notice())

ac = AccessControl()

admin = Administrator("Admin1", "1ts2He11", ["control_panel", "manage_users"])
user = RegularUser("ShevViol79", "4ufD31")
guest = GuestUser()

ac.add_user(admin)
ac.add_user(user)
ac.add_user(guest)

result1 = ac.authenticate_user("ShevViol79", "wrong_pass")
print(result1)

result2 = ac.authenticate_user("ShevViol79", "4ufD31")
print(result2)

if result2:
    print(f"Ви ввійшли як {result2.username}")

result3 = ac.authenticate_user("Admin11", "1ts2He11")
print(result3)

result4 = ac.authenticate_user("Admin1", "1ts2He11")
print(result4)

if result4:
    print(f"Ви ввійшли як {result4.username}")

new_user = RegularUser("PerAndr356", "Rou781ine")
ac.add_user(new_user, by_admin=result4)
