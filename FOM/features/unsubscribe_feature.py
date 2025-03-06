# from common.feature_constant import FEATURES
# from common.models.feature import Feature, ClientFeature, BranchDepartmentFeature
from .models import CommonBranchDepartmentFeature, CommonFeature , CommonClientFeature

def unsubscribe_feature_name():
    features = CommonFeature.objects.all()
    return {
        'features' : features
    }


def unsubscribe_feature(feature_name: str):
    feature = CommonFeature.objects.get(name=feature_name)
    value_to_set = feature.default_value
    CommonClientFeature.objects.filter(feature_id=feature.id).update(feature_value=value_to_set)
    CommonBranchDepartmentFeature.objects.filter(feature_id=feature.id).update(feature_value=value_to_set)
    # print(feature_name)
    # try:

    #     feature = Feature.objects.get(name=feature_name)
    #     value_to_set = FEATURES[feature.name]['default_value']
    #     ClientFeature.objects.filter(feature_id=feature.id).update(feature_value=value_to_set)
    #     BranchDepartmentFeature.objects.filter(feature_id=feature.id).update(feature_value=value_to_set)

    # except Exception as e:
    #     return e
    return "Feature unsubscribed successfully"
