from django.db import models

# models
# NOTES :MIssing :  Common branch master : branch_id = models.ForeignKey('CommonBranchMaster', on_delete=models.CASCADE)
# And : department_id = models.ForeignKey('CommonDepartment', on_delete=models.CASCADE)

class CommonClient(models.Model):
    #  Note : just for random insertion unique = false done , after that  change it to True
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField()
    lot_prefix = models.CharField(max_length=50)
    #  Note : just for random insertion unique = false done , after that  change it to True
    username_prefix_code = models.CharField(max_length=50, unique=True)
    dispatch_date_freeze = models.DateTimeField()
    formal_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class CommonClientFeature(models.Model):
    feature_value = models.TextField() 
    client = models.ForeignKey(CommonClient, on_delete=models.CASCADE)
    feature_id = models.ForeignKey('CommonFeature', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('client', 'feature_id'),)

class CommonBranchDepartmentFeature(models.Model):
    feature_value = models.TextField()
    branch_id = models.IntegerField(10)  #need changes
    client = models.ForeignKey(CommonClient, on_delete=models.CASCADE)
    department_id = models.IntegerField(10)  #need changes
    feature = models.ForeignKey('CommonFeature', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('client', 'branch_id', 'department_id', 'feature'),)
        
class CommonFeature(models.Model):
    #Note change uniue = true after this is false just for random data check
    name = models.CharField(max_length=100, unique=True)
    default_value = models.TextField()
    value_type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Branches(models.Model):
    branch_name = models.CharField(max_length=255)
    client = models.ForeignKey(CommonClient, on_delete=models.CASCADE)
    def __str__(self):
        return self.branch_name
    

class Departments(models.Model):
    department_name = models.CharField(max_length=255)
    client = models.ForeignKey(CommonClient, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.department_name
