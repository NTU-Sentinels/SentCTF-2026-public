class SessionUser:
    def __init__(self, user_uid=None, user_cn=None, user_sn=None, user_employeeNumber=None, user_mail=None, user_title=None, employeeType=None):
        self.uid = user_uid
        self.cn = user_cn
        self.sn = user_sn
        self.employeeNumber = user_employeeNumber
        self.mail = user_mail
        self.title = user_title
        self.employeeType = employeeType

    def clear(self):
        # Clear the session user attributes
        self.uid = None
        self.cn = None
        self.sn = None
        self.employeeNumber = None
        self.mail = None
        self.title = None
        self.employeeType = None

class LdapSession:
    def __init__(self, role=None, uid=None, cn=None, sn=None, employeeNumber=None, mail=None, title=None):
        self.role = role
        self.sessionuser = SessionUser(user_uid=uid, user_cn=cn, user_sn=sn, user_employeeNumber=employeeNumber, user_mail=mail, user_title=title, employeeType=role)

    def clear(self):
        # Clear the session on the server side
        self.role = None
        self.sessionuser.clear()

class SamlSession:
    def __init__(self, role=None, name_id=None, session_index=None, uid=None, cn=None, sn=None, employeeNumber=None, mail=None, title=None):
        self.role = role
        self.name_id = name_id
        self.session_index = session_index
        self.sessionuser = SessionUser(user_uid=uid, user_cn=cn, user_sn=sn, user_employeeNumber=employeeNumber, user_mail=mail, user_title=title, employeeType=role)  # Assuming role is used as employeeType for SAML sessions

    def clear(self):
        # Clear the session on the server side
        self.role = None
        self.name_id = None
        self.session_index = None
        self.sessionuser.clear()