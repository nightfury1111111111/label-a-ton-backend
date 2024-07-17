from bson import ObjectId
from apps.user.models import User


def snake_to_camel(snake_str):
    if snake_str == "_id":
        return "id"
    components = snake_str.split("_")
    camel_str = components[0] + "".join(x.capitalize() for x in components[1:])
    return camel_str


def convert_db_data_to_json(data):
    data_dict = data.to_mongo().to_dict()
    for key, value in data_dict.items():
        if isinstance(value, ObjectId):
            data_dict[key] = str(value)

    camel_case_data = {snake_to_camel(k): v for k, v in data_dict.items()}
    return camel_case_data


def get_relevant_taskers():
    # Aggregation pipeline
    pipeline = [
        {
            "$match": {"register_flag": True}
        },  # Stage to filter documents where register_flag is True
        {"$sample": {"size": 3}},  # Stage to randomly select up to 3 documents
    ]

    # Execute the aggregation pipeline
    random_users = User.objects.aggregate(*pipeline)

    # Extracting the IDs
    random_user_ids = [str(user["_id"]) for user in random_users]

    return random_user_ids

def get_relevant_tasker():
    # Aggregation pipeline
    pipeline = [
        {
            "$match": {"register_flag": True}
        },  # Stage to filter documents where register_flag is True
        {"$sample": {"size": 3}},  # Stage to randomly select up to 3 documents
    ]

    # Execute the aggregation pipeline
    random_users = User.objects.aggregate(*pipeline)

    # Extracting the IDs
    random_user_ids = [str(user["_id"]) for user in random_users]

    return random_user_ids[0]
