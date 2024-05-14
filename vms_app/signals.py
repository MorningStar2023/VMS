from django.db.models.signals import pre_save
from django.dispatch import receiver


# @receiver(pre_save, sender=Productivity)
# def calculate_estimation(sender, instance, **kwargs):
#     total_estimation = 0
#     for route in instance.routes.all():
#         total_estimation += route.estimation
#     instance.estimation = total_estimation
