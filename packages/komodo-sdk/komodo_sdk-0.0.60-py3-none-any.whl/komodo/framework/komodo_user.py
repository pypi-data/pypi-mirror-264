class KomodoUser:
    def __init__(self, *, email, name, **kwargs):
        self.email = email
        self.name = name
        self.role = kwargs.get('role', 'user')
        self.plan = kwargs.get('plan', 'free')
        self.verified = kwargs.get('verified', False)
        self.allowed_assistants = kwargs.get('allowed_assistants', [])
        self.preferred_assistant = kwargs.get('preferred_assistant', '')
        self.show_tool_progress = kwargs.get('show_tool_progress', None)

    def __str__(self):
        return f"KomodoUser(email={self.email}, name={self.name}, " \
               f"role={self.role}, plan={self.plan}, verified={self.verified}, " \
               f"allowed_assistants={self.allowed_assistants}, preferred_assistant={self.preferred_assistant})"

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'plan': self.plan,
            'verified': self.verified,
            'allowed_assistants': self.allowed_assistants,
            'preferred_assistant': self.preferred_assistant,
            'show_tool_progress': self.show_tool_progress}

    @staticmethod
    def default():
        email = "ryan.oberoi@komodoapp.ai"
        return KomodoUser(email=email, name="Ryan Oberoi")

    @staticmethod
    def poweruser():
        email = "ryan@kmdo.app"
        return KomodoUser(email=email, name="Ryan", show_tool_progress="details")
