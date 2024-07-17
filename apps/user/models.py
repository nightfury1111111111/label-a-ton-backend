from mongoengine import *
import datetime  # Import datetime module


# Create your models here.
class Feedback(EmbeddedDocument):
    task_id = StringField(default="")
    is_feedback = BooleanField(default=False)
    rate = FloatField(required=True, min_value=1, max_value=5)
    content = StringField()


class User(Document):
    meta = {"collection": "users"}
    solana_address = StringField(max_length=100, unique=True, verbose_name="Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", default="")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance", default=0)
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    # field for tasker or requester -> if True tasker, otherwise Requester
    register_flag = BooleanField(default=False, verbose_name="Register Flag")
    # fields for taskers
    register_step = StringField(
        max_length=30, verbose_name="Register Step", default="0"
    )
    name = StringField(max_length=30, verbose_name="Name", default="")
    avatar = StringField(verbose_name="Avatar", default="")
    nation = StringField(max_length=30, verbose_name="Nation", default="")
    is_dao_member = BooleanField(default=False, verbose_name="Is Dao Member")
    daos = ListField(StringField(), default=[])
    skills = ListField(StringField(), default=[])
    desired_skills = ListField(StringField(), default=[])
    agents = ListField(StringField(), default=[])
    work_history = ListField(StringField(), default=[])

    # fields for tasker career
    total_earnings = FloatField(default=0.0)
    total_jobs = IntField(default=0)
    hourly_rate = FloatField(default=0)
    feedbacks = ListField(EmbeddedDocumentField(Feedback), default=[])
    rejected_jobs = IntField(default=0)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(
        default=datetime.datetime.now, update=datetime.datetime.now
    )
    deleted_at = DateTimeField(default=None)

    @staticmethod
    def get_by_solana_address(address):
        try:
            return User.objects(solana_address=address).first()
        except DoesNotExist:
            return None

    def soft_delete(self):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None


class Requester(Document):
    meta = {"collection": "requesters"}
    email = EmailField(verbose_name="Email Address", required=False)
    password = StringField(required=False)
    register_step = StringField(max_length=30, verbose_name="Register Step")
    register_flag = BooleanField(required=False)
    name = StringField(max_length=30, verbose_name="Name")
    first_name = StringField(max_length=30, verbose_name="First Name")
    last_name = StringField(max_length=30, verbose_name="Last Name")
    date_of_birth = DateTimeField(verbose_name="Date of Birth")
    biography = StringField(verbose_name="Biography")
    profile_picture = StringField(verbose_name="Profile Picture")
    solanaAddress = StringField(max_length=100, verbose_name="Address")
    ethereumAddress = StringField(max_length=100, verbose_name="Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", required=False)
    role = StringField(max_length=20, verbose_name="Role")
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance")
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()


class Tasker(Document):
    meta = {"collection": "taskers"}
    email = EmailField(verbose_name="Email Address", required=False)
    password = StringField(required=False)
    register_step = StringField(max_length=30, verbose_name="Register Step")
    register_flag = BooleanField(required=False)
    name = StringField(max_length=30, verbose_name="Name", default="")
    avatar = StringField(verbose_name="Avatar")
    nation = StringField(max_length=30, verbose_name="Nation")
    is_dao_member = BooleanField(max_length=30, verbose_name="Is Dao Member")
    daos = ListField(StringField())
    skills = ListField(StringField())
    desired_skills = ListField(StringField())
    agents = ListField(StringField())
    first_name = StringField(max_length=30, verbose_name="First Name")
    last_name = StringField(max_length=30, verbose_name="Last Name")
    date_of_birth = DateTimeField(verbose_name="Date of Birth")
    biography = StringField(verbose_name="Biography")
    profile_picture = StringField(verbose_name="Profile Picture")
    solanaAddress = StringField(max_length=100, verbose_name="Solana Address")
    ethereumAddress = StringField(max_length=100, verbose_name="Ethereum Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", required=False)
    role = StringField(max_length=20, verbose_name="Role")
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance")
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
