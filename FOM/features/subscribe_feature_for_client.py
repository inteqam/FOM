import ast

from django.core import exceptions

# from common.models import Client
# from common.models.feature import Feature, ClientFeature, FEATURE_TYPE_SWITCHER
from .models import CommonClient, CommonClientFeature,CommonFeature

def subscribe_feature_client():

    clients = CommonClient.objects.all()
    features = CommonFeature.objects.all()

    return {
        'clients' : clients,
        'features' : features
    }
def subscribe_feature_for_client(client_name: str, feature_name: str, feature_value: str = None):
    # print(client_name,feature_name,feature_value)
#     try:
#         client = Client.objects.get(name=client_name)
#         feature_to_subscribe = Feature.objects.get(name=feature_name)

#         data_type = FEATURE_TYPE_SWITCHER.get(feature_to_subscribe.value_type)
#         if feature_value and not isinstance(ast.literal_eval(feature_value), data_type):
#             return exceptions.ValidationError(f'feature_value must be of type {feature_to_subscribe.value_type}')

#         client_feature = ClientFeature.objects.filter(client=client, feature=feature_to_subscribe)

#         if client_feature:
#             client_feature.update(feature_value=feature_value)
#         else:
#             ClientFeature.objects.create(client_id=client.id,
#                                          feature_id=feature_to_subscribe.id,
#                                          feature_value=str(feature_value))
#         return True
#     except Exception as e:
#         return e
    feature_id = CommonFeature.objects.get(name=feature_name).id
    client_id = CommonClient.objects.get(name=client_name).id

    CommonClientFeature.objects.create(
            client_id=client_id,
            feature_id_id=feature_id,
            feature_value=feature_value,
        )
    return "Feature subscribed successfully"