class UnknownRoleException(Exception):
    def __init__(self, role_name: str):
        self.role_name = role_name
        self.message = f"Unknown role: {role_name}"
        super().__init__(self.message)
