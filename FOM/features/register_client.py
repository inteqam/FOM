from common.models import Client
from common.models.feature import Feature, ClientFeature


def register_client(client_name: str):
    client_name_upper = client_name.upper()
    client_info = Client.objects.get_or_create(name=client_name_upper)
    client = client_info[0]

    existing_client_features = ClientFeature.objects.filter(client=client).values_list('feature_id', flat=True)
    features = Feature.objects.values_list('id', flat=True)

    features_to_insert_for_client = list(set(features) - set(existing_client_features))
    client_features = (ClientFeature(client=client, feature_id=feature_id)
                       for feature_id in features_to_insert_for_client)
    ClientFeature.objects.bulk_create(client_features)
