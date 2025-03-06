from django.db import transaction
# from common.feature_constant import FEATURES
# from common.models.feature import Feature


@transaction.atomic()
def insert_features() -> None:
    print("insert_features called.")
    # existing_feature_names: [str] = Feature.objects.all().values_list('name', flat=True)
    # features_to_create: [Feature] = []
    # feature_names_to_create: [str] = []

    # for feature_name, feature_info in FEATURES.items():
    #     if feature_name not in existing_feature_names:
    #         if not feature_info.get('description'):
    #             raise Exception("You need to specify a description.")

    #         features_to_create.append(Feature(name=feature_name, **feature_info))
    #         feature_names_to_create.append(feature_name)

    # print("New Features -")
    # print(f"({', '.join(feature_names_to_create)}) \n")
    # Feature.objects.bulk_create(features_to_create)

    return "Feature Inserted Successfully"
