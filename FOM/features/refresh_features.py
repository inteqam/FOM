from django.db import transaction
from django.db.models import QuerySet
# from aes.queryset_utils import convert_queryset_values_to_dict
# from common.feature_constant import FEATURES
# from common.models import Feature


@transaction.atomic
def refresh_features() -> None:
    # existing_features: QuerySet[Feature] = Feature.objects.all()
    # existing_features_data_map: dict = convert_queryset_values_to_dict(queryset=existing_features,
    #                                                                    key_name='name')
    # print(f"Total features in DB: {len(existing_features_data_map)}")

    # existing_feature_names: set[str] = {existing_feature.name for existing_feature in existing_features}
    # mapping_feature_names: set[str] = {feature_name for feature_name in FEATURES.keys()}
    # features_name_to_remove: set[str] = existing_feature_names - mapping_feature_names
    # features_id_to_remove: set[int] = set()
    # features_to_update: [Feature] = []

    # print(f"Features which are removing from DB -")
    # print(f"({', '.join(features_name_to_remove)})")

    # for feature_name_to_remove in features_name_to_remove:
    #     existing_feature_obj: Feature = existing_features_data_map.pop(feature_name_to_remove)
    #     features_id_to_remove.add(existing_feature_obj.pk)

    # print(f"\nRemoving features from DB..")
    # Feature.objects.filter(id__in=features_id_to_remove).delete()

    # print("Refreshing features content..")
    # for feature_name, feature_info in FEATURES.items():
    #     existing_feature_obj: Feature = existing_features_data_map[feature_name]
    #     if existing_feature_obj.description != feature_info['description']:
    #         existing_feature_obj.description = feature_info['description']
    #         features_to_update.append(existing_feature_obj)

    # print(f"Updating features in DB.. \n")
    # Feature.objects.bulk_update(objs=features_to_update, fields=('description', ),
    #                             batch_size=250)

    return "Features Refreshed"
