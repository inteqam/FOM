from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CommonClient, CommonBranchDepartmentFeature, Branches, Departments, CommonClientFeature, CommonFeature
from .insert_features import insert_features
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import FeatureForm
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
import json
from .unsubscribe_feature import unsubscribe_feature, unsubscribe_feature_name
from .subscribe_feature_for_branch_department import sub_fea_branch_department, subscribe_feature_for_branch_department
from .subscribe_feature_for_client import subscribe_feature_for_client, subscribe_feature_client
from .refresh_features import refresh_features


def index(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        match str(choice):
            case '1':
                return render(request, 'register_client.html')
            case '2':
                msg = insert_features()
                messages.success(request, msg)
                # here i want to show popup feature here that inseret feature succesfully
                return render(request, 'index.html')
            case '3':
                context = subscribe_feature_client()
                return render(request, 'subcribe_feature_client.html', context)
            case '4':
                context = sub_fea_branch_department()
                return render(request, 'sub_feat_branch&department.html', context)
            case '5':
                context = unsubscribe_feature_name()
                return render(request, 'unsubcribe_feature.html',context)
            case '6':
                msg = refresh_features()
                messages.success(request, msg)
                return render(request, 'index.html')
            case '7':
                
                return redirect('display_feature')
            case _:
                return render(request, 'index.html', {"error": True})

    # message =  request.COOKIES.get('message')
    # if message:
    #     return render(request, 'index.html', {"error": False,"message":message})
    return render(request, 'index.html', {"error": False})


def list_clients(request):
    clients = CommonClient.objects.all()
    return render(request, 'clients_list.html', {'clients': clients})


@csrf_exempt
def register_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        active = request.POST.get('active') == 'on'
        lot_prefix = request.POST.get('lot_prefix')
        username_prefix_code = request.POST.get('username_prefix_code')
        dispatch_date_freeze = request.POST.get('dispatch_date_freeze')
        formal_name = request.POST.get('formal_name')

        CommonClient.objects.create(
            name=name,
            active=active,
            lot_prefix=lot_prefix,
            username_prefix_code=username_prefix_code,
            dispatch_date_freeze=dispatch_date_freeze,
            formal_name=formal_name
        )
        return redirect('clients_list')
    return render(request, 'register_client.html')


@csrf_exempt
def edit_client(request, client_id):
    client = get_object_or_404(CommonClient, id=client_id)
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.active = request.POST.get('active') == 'on'
        client.lot_prefix = request.POST.get('lot_prefix')
        client.username_prefix_code = request.POST.get('username_prefix_code')
        client.dispatch_date_freeze = request.POST.get('dispatch_date_freeze')
        client.formal_name = request.POST.get('formal_name')
        client.save()
        return redirect('clients_list')
    return render(request, 'edit_client.html', {'client': client})


@csrf_exempt
def subcribe_feature_for_client(request):
    context = subscribe_feature_client()
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        feature_name = request.POST.get('feature_name')
        feature_value = request.POST.get('feature_value')
        # CommonClientFeature.objects.create(
        #     client_id=client_name,
        #     feature_id=feature_name,
        #     feature_value=feature_value,
        # )
        msg = subscribe_feature_for_client(client_name, feature_name, feature_value)
        # messages.success(request, msg)
        # request.session['message'] = msg

        messages.success(request, msg)
        return redirect('index')
    return render(request, 'subcribe_feature_client.html', context)


@csrf_exempt
def subscribe_feature_for_branch_department_view(request):
    context = sub_fea_branch_department()
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        branch_id = request.POST.get('branch_id')
        department_id = request.POST.get('department_id')
        feature_name = request.POST.get('feature_name')
        feature_value = request.POST.get('feature_value')
        # CommonBranchDepartmentFeature.objects.create(
        #     client_id=client_id,
        #     branch_id=branch_id,
        #     department_id=department_id,
        #     feature_name=feature_name,
        #     feature_value=feature_value,
        # )
        msg = subscribe_feature_for_branch_department(
            client_id, branch_id, department_id, feature_name, feature_value)
        messages.success(request, msg)
        return redirect('index')
    return render(request, 'sub_feat_branch&department.html', context)


def unsubcribe_feature(request):
    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')
        msg = unsubscribe_feature(feature_name)
        messages.success(request, msg)
        return redirect('index')
    return render(request, 'unsubcribe_feature.html')


# for features
class FeatureListView(View):
    template_name = 'features/feature_list.html'

    def get(self, request):
        # Fetching data from CommonFeature model
        common_features = CommonFeature.objects.all()
        combined_features = []
        for feature in common_features:
            combined_features.append({
                'id': feature.pk,
                'name': feature.name,
                'default_value': feature.default_value,  # Correct field name
                'value_type': feature.value_type,  # Correct field name
                'description': feature.description,  # Correct field name
                'type': 'common'
            })

        context = {
            'features': combined_features
        }
        return render(request, self.template_name, context)


class FeatureCreateView(CreateView):
    model = CommonFeature
    form_class = FeatureForm
    template_name = 'features/feature_form.html'
    success_url = reverse_lazy('feature_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add logic to handle different feature types (client, branch_department)
        return response


class FeatureUpdateView(UpdateView):
    model = CommonFeature
    form_class = FeatureForm
    template_name = 'features/feature_form.html'
    success_url = reverse_lazy('feature_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add logic to handle different feature types (client, branch_department)
        return response


class FeatureDeleteView(DeleteView):
    model = CommonFeature
    template_name = 'features/feature_confirm_delete.html'
    success_url = reverse_lazy('feature_list')


def blank_page_view(request):
    return render(request, 'blank_page.html')

# new


@csrf_exempt
def update_feature_description(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feature_id = data.get('id')
        description = data.get('description')
        try:
            feature = CommonFeature.objects.get(id=feature_id)
            feature.description = description
            feature.save()
            return JsonResponse({'success': True})
        except CommonFeature.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Feature not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def blank_page_view(request):
    return render(request, 'blank_page.html')

# new


@csrf_exempt
def update_feature_description(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feature_id = data.get('id')
        description = data.get('description')
        try:
            feature = CommonFeature.objects.get(id=feature_id)
            feature.description = description
            feature.save()
            return JsonResponse({'success': True})
        except CommonFeature.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Feature not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def display_feature(request):
    context = sub_fea_branch_department()
    if request.method == 'POST':
        # department_id = 1
        # feature_id = 1
        # branch_id = 1
        # client_id = 4
        # model_name = 'CommonBranchDepartmentFeature'
        # model_name = 'CommonFeature'
        # model_name = 'CommonClientFeature'
        model_name = request.POST.get('model_name')
        branch_id = request.POST.get('branch_id')
        department_id = request.POST.get('department_id')
        feature_name = request.POST.get('feature_name')
        if model_name == 'CommonClientFeature':
            result = []
            client_id = request.POST.get('client_id')
            # print(client_id)
            data = CommonClientFeature.objects.filter(client_id=client_id)
            print(data)
            for item in data:
                client_name = CommonClient.objects.get(id=item.client_id).name
                feature_name = CommonFeature.objects.get(id=item.feature_id_id).name
                feature_value = item.feature_value
                result.append({
                    'client_name': client_name,
                    'feature_name': feature_name,
                    'feature_value' : feature_value
                })
            context = {
                'result': result
            }
            return render(request,'list_commonclientfeature.html',context)
        if model_name == 'CommonBranchDepartmentFeature':
            result = []
            client_id = request.POST.get('bnd_client_id')
            print(client_id)
            data = CommonBranchDepartmentFeature.objects.filter(department_id=department_id, branch_id=branch_id, client_id=client_id)
            for item in data:
                client_name = CommonClient.objects.get(id=item.client_id).name
                branch_name = Branches.objects.get(id=item.branch_id).branch_name
                department_name = Departments.objects.get(id=item.department_id).department_name
                feature_name = CommonFeature.objects.get(id=item.feature_id).name
                feature_value = CommonBranchDepartmentFeature.objects.get(id=item.client_id).feature_value

                result.append({
                    'client_name': client_name,
                    'branch_name': branch_name,
                    'department_name': department_name,
                    'feature_name': feature_name,
                    'feature_value': feature_value
                })
            context = {
                'result': result
                }
            return render(request,'list_commonbranchdepartmentfeature.html',context)
        if model_name == 'CommonFeature':
            feature_id = CommonFeature.objects.get(name=feature_name).id
            result1 = []
            result2 = []
            result3 = []
            data1 = CommonBranchDepartmentFeature.objects.filter(feature_id=feature_id)
            data2 = CommonClientFeature.objects.filter(feature_id=feature_id)
            data3 = CommonFeature.objects.filter(name=feature_name)
            print(data3)
            for item in data1:
                client_name = CommonClient.objects.get(id=item.client_id).name
                branch_name = Branches.objects.get(id=item.branch_id).branch_name
                department_name = Departments.objects.get(id=item.department_id).department_name
                feature_name = CommonFeature.objects.get(id=item.feature_id).name
                feature_value = item.feature_value


                result1.append({
                    'client_name': client_name,
                    'branch_name': branch_name,
                    'department_name': department_name,
                    'feature_name': feature_name,
                    'feature_value': feature_value
                })
            for item in data2:
                client_name = CommonClient.objects.get(id=item.client_id).name
                feature_name = CommonFeature.objects.get(id=item.feature_id_id).name
                feature_value = item.feature_value


                result2.append({
                    'client_name': client_name,
                    'feature_name': feature_name,
                    'feature_value' : feature_value
                })
        for item in data3:
            name = item.name
            default_value = item.default_value
            value_type = item.value_type
            description = item.description

            result3.append({
            'name': name,
            'default_value': default_value,
            'value_type': value_type,
            'description': description
            })
            # print(result3)
            context = {
            'result1': result1,
            'result2': result2,
            'result3': result3
            }
            return render(request,'list_commonfeature.html',context)
    return render(request, 'display_feature.html', context)



def list_commonfeature(request):
    return render(request,'list_commonfeature.html')

def list_commonbranchdepartmentfeature(request):
    return render(request,'list_commonbranch&depfeature.html')

def list_commonclientfeature(request):
    result = request.session.pop("result")
    context = {
        'result': result
    }
    return render(request,'list_commonclientfeature.html',context)
