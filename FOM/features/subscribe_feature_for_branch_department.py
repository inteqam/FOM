import ast
import json

from django.core import exceptions

# from common.models import DepartmentBranchMapping
# from common.models.feature import Feature, FEATURE_TYPE_SWITCHER, BranchDepartmentFeature
from .models import CommonClient,CommonBranchDepartmentFeature,Branches,Departments,CommonFeature

def sub_fea_branch_department():

    clients = CommonClient.objects.all()
    branches = Branches.objects.all()
    departments = Departments.objects.all()
    features = CommonFeature.objects.all()
    client_dict = {}
    branch_dict = {}

    for client in clients:
        client_branches = list(branches.filter(client_id=client.id).values('id', 'branch_name'))
        # client_departments = list(departments.filter(client_id=client.id).values('id', 'department_name'))
    
        client_dict[client.id] = {
            'branches': list(client_branches),
            # 'departments': client_departments
        }
    for branch in branches:
        branch_departments = list(departments.filter(branch_id=branch.id).values('id', 'department_name'))

        branch_dict[branch.id] = {
            'departments': list(branch_departments)
        }
    
    return {
        'clients' : clients,
        'client_dict': json.dumps(client_dict),
        'branch_dict' : json.dumps(branch_dict),
        'features' : features
    }
def subscribe_feature_for_branch_department(client_id: int,
                                            branch_id: int, department_id: int, feature_name: str,
                                            feature_value: str = None):
    # print(client_id,branch_id,department_id,feature_name,feature_value)
#     try:
#         mapping = DepartmentBranchMapping.objects.filter(branch_id=branch_id, department_id=department_id)
#         if not mapping:
#             return exceptions.ValidationError(f'Mapping does not exist.')

#         feature_to_subscribe = Feature.objects.get(name=feature_name)

#         data_type = FEATURE_TYPE_SWITCHER.get(feature_to_subscribe.value_type)
#         if feature_value and not isinstance(ast.literal_eval(feature_value), data_type):
#             return exceptions.ValidationError(f'feature_value must be of type {feature_to_subscribe.value_type}')

#         branch_department_feature = BranchDepartmentFeature.objects.filter(branch_id=branch_id,
#                                                                            department_id=department_id,
#                                                                            feature=feature_to_subscribe)

#         if branch_department_feature:
#             branch_department_feature.update(feature_value=feature_value)
#         else:
#             BranchDepartmentFeature.objects.create(client_id=client_id,
#                                                    branch_id=branch_id,
#                                                    department_id=department_id,
#                                                    feature=feature_to_subscribe,
#                                                    feature_value=feature_value)

#         return True
#     except Exception as e:
#         return e
    feature_id = CommonFeature.objects.get(name=feature_name).id

    CommonBranchDepartmentFeature.objects.create(
            client_id=client_id,
            branch_id=branch_id,
            department_id=department_id,
            feature_id=feature_id,
            feature_value=feature_value,
        )
    return "Feature Subscribe For Branch Successful"