# import ast

# from django.core import exceptions
# from django.db import models

# from aes import CLIENT_FEATURES
# from aes.customs.custom_models import CustomClientAwareModel, ErpModel
# from aes.queryset_utils import convert_model_list_to_nested_dict
# from common.models.account_masters import BranchMaster, Department, DepartmentBranchMapping
# from common.models.client import Client


# class FeatureTypeChoices(models.TextChoices):
#     DICT = "dict"
#     LIST = "list"
#     INT = "int"
#     BOOL = "bool"
#     STRING = 'str'
#     FLOAT = 'float'


# FEATURE_TYPE_SWITCHER = {
#     'dict': dict,
#     'list': list,
#     'int': int,
#     'bool': bool,
#     'str': str,
#     'float': float,
# }


# class Feature(ErpModel):
#     name = models.CharField(unique=True, max_length=100)
#     default_value = models.TextField()
#     value_type = models.CharField(choices=FeatureTypeChoices.choices, max_length=5)
#     description = models.TextField(null=True)

#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         data_type = FEATURE_TYPE_SWITCHER.get(self.value_type, str)
#         if not isinstance(ast.literal_eval(self.default_value), data_type):
#             return exceptions.ValidationError(f'default_value must be of type {self.value_type}')
#         # Feature name must be in CAPS
#         self.name = str(self.name).upper()
#         super(Feature, self).save(force_insert, force_update, using, update_fields)


# class ClientFeature(CustomClientAwareModel):
#     client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='client_feature_list')
#     feature = models.ForeignKey(to=Feature, on_delete=models.CASCADE)
#     feature_value = models.TextField(null=True, default=None)

#     class Meta:
#         constraints = [models.constraints.UniqueConstraint(fields=('client', 'feature'),
#                                                            name='client_feature_uniqueness'), ]

#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         data_type = FEATURE_TYPE_SWITCHER.get(self.feature.value_type, str)
#         if self.feature_value and not isinstance(ast.literal_eval(self.feature_value),
#                                                  data_type):
#             return exceptions.ValidationError(f'feature_value must be of type {self.feature.value_type}')
#         return super(ClientFeature, self).save(force_insert, force_update, using, update_fields)


# class BranchDepartmentFeature(CustomClientAwareModel):
#     branch = models.ForeignKey(to=BranchMaster, on_delete=models.CASCADE)
#     department = models.ForeignKey(to=Department, on_delete=models.CASCADE)
#     feature = models.ForeignKey(to=Feature, on_delete=models.CASCADE)
#     feature_value = models.TextField(null=True, default=None)

#     class Meta:
#         constraints = [models.constraints.UniqueConstraint(fields=('client', 'branch', 'department', 'feature'),
#                                                            name='branch_department_feature_uniqueness'), ]

#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         data_type = FEATURE_TYPE_SWITCHER.get(self.feature.value_type, str)
#         if self.feature_value and not isinstance(ast.literal_eval(self.feature_value),
#                                                  data_type):
#             return exceptions.ValidationError(f'feature_value must be of type {self.feature.value_type}')
#         return super(BranchDepartmentFeature, self).save(force_insert, force_update, using, update_fields)


# def get_client_features():
#     branch_department_features_qs = BranchDepartmentFeature.objects.all()
#     client_features_qs = ClientFeature.objects.all()
#     features_qs = Feature.objects.all()

#     branch_department_features = {}
#     for branch_department_feature in branch_department_features_qs:
#         branch_id = branch_department_feature.branch_id
#         department_id = branch_department_feature.department_id
#         feature_id = branch_department_feature.feature_id
#         branch_department_features[(branch_id, department_id, feature_id)] = branch_department_feature.feature_value
#     client_features = {}
#     for client_feature in client_features_qs:
#         client_id = client_feature.client_id
#         feature_id = client_feature.feature_id
#         client_features[(client_id, feature_id)] = client_feature.feature_value

#     features = {}
#     for feature in features_qs:
#         value_type = feature.value_type
#         default_value = feature.default_value

#         data_type = FEATURE_TYPE_SWITCHER.get(value_type, str)
#         string_feature_value_to_use = default_value
#         """
#         Note : Syntax ast.literal_eval(node or string)
#         Node means any file or string means you data with data type in '' or ""
#         ast.literal_eval('True')  verify because it understand True is bool type of data
#         ast.literal_eval('[1,2]') verify  because it understand [1,2] is list type data
#         ast.literal_eval('abc') failed 
#         it verify if ast.literal_eval("'abc'") now verify because  it understand 'abc' is string type of data 
#         for more understanding  ast.literal_eval refer 
#         https://www.aipython.in/python-literal_eval/#:~:text=Python%20literal_eval%20is%20a%20function,of%20built%2Din%20class%20library.&text=The%20ast%20module%20helps%20Python,Python%20literal%20or%20container%20display
#         """
#         feature_value_to_use = data_type(ast.literal_eval(string_feature_value_to_use))

#         features[feature.id] = {'value_type': value_type, 'value_to_use': feature_value_to_use, 'name': feature.name}

#     branch_department_mappings = DepartmentBranchMapping.objects.all()
#     data = []

#     for branch_department_mapping in branch_department_mappings:
#         branch_id = branch_department_mapping.branch_id
#         department_id = branch_department_mapping.department_id
#         client_id = branch_department_mapping.department.client_id
#         client_name = branch_department_mapping.department.client.name

#         for feature_id, feature in features.items():
#             value_type = feature['value_type']
#             feature_value_to_use = feature['value_to_use']
#             feature_name = feature['name']

#             branch_department_key = (branch_id, department_id, feature_id)
#             client_key = (client_id, feature_id)
#             if branch_department_key in branch_department_features:
#                 feature_value = branch_department_features[branch_department_key]
#                 data_type = FEATURE_TYPE_SWITCHER.get(value_type, str)
#                 string_feature_value_to_use = feature_value
#                 feature_value_to_use = data_type(ast.literal_eval(string_feature_value_to_use))
#             elif client_key in client_features:
#                 feature_value = client_features[client_key]
#                 data_type = FEATURE_TYPE_SWITCHER.get(value_type, str)
#                 string_feature_value_to_use = feature_value
#                 feature_value_to_use = data_type(ast.literal_eval(string_feature_value_to_use))

#             info = {
#                 'client_name': client_name,
#                 'branch_id': str(branch_id),
#                 'department_id': str(department_id),
#                 'feature_name': feature_name,
#                 'feature_value': feature_value_to_use,
#             }
#             data.append(info)
#     result = convert_model_list_to_nested_dict(data, 'feature_value', 'feature_name', 'department_id',
#                                                'branch_id', 'client_name')
#     CLIENT_FEATURES.update(**result)
#     return


# def get_client_features_for_client():
#     client_features_qs = ClientFeature.objects.all()
#     features_qs = Feature.objects.all()

#     client_features = {}
#     for client_feature in client_features_qs:
#         client_id = client_feature.client_id
#         feature_id = client_feature.feature_id
#         client_features[(client_id, feature_id)] = client_feature.feature_value

#     features = {}
#     for feature in features_qs:
#         value_type = feature.value_type
#         default_value = feature.default_value

#         data_type = FEATURE_TYPE_SWITCHER.get(value_type, str)
#         string_feature_value_to_use = default_value
#         """
#         Note : Syntax ast.literal_eval(node or string)
#         Node means any file or string means you data with data type in '' or ""
#         ast.literal_eval('True')  verify because it understand True is bool type of data
#         ast.literal_eval('[1,2]') verify  because it understand [1,2] is list type data
#         ast.literal_eval('abc') failed 
#         it verify if ast.literal_eval("'abc'") now verify because  it understand 'abc' is string type of data 
#         for more understanding  ast.literal_eval refer 
#         https://www.aipython.in/python-literal_eval/#:~:text=Python%20literal_eval%20is%20a%20function,of%20built%2Din%20class%20library.&text=The%20ast%20module%20helps%20Python,Python%20literal%20or%20container%20display
#         """
#         feature_value_to_use = data_type(ast.literal_eval(string_feature_value_to_use))

#         features[feature.id] = {'value_type': value_type, 'value_to_use': feature_value_to_use, 'name': feature.name}

#     data = {}

#     for client in Client.objects.all():
#         client_id = client.id
#         client_name = client.name
#         data[client_name] = {}

#         for feature_id, feature in features.items():
#             value_type = feature['value_type']
#             feature_value_to_use = feature['value_to_use']
#             feature_name = feature['name']

#             client_key = (client_id, feature_id)

#             if client_key in client_features:
#                 feature_value = client_features[client_key]
#                 data_type = FEATURE_TYPE_SWITCHER.get(value_type, str)
#                 string_feature_value_to_use = feature_value
#                 feature_value_to_use = data_type(ast.literal_eval(string_feature_value_to_use))

#             data[client_name][feature_name] = feature_value_to_use

#     return data
