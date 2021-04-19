from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "HomeOwner"), (3, "Staff"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Gender(models.Model):
    gen = models.CharField(max_length=10)
    objects = models.Manager()


class Relation(models.Model):
    category = models.CharField(max_length=20)
    objects = models.Manager()


class HouseNumber(models.Model):
    hse_number = models.PositiveSmallIntegerField()
    objects = models.Manager()


class Position(models.Model):
    title = models.CharField(max_length=20)
    objects = models.Manager()


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class HomeOwner(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    identity_number = models.PositiveIntegerField()
    mobile_number = models.PositiveIntegerField()
    house_number = models.ForeignKey(HouseNumber, on_delete=models.CASCADE)
    profile_picture = models.FileField()
    objects = models.Manager()


class Residents(models.Model):
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    category = models.ForeignKey(Relation, on_delete=models.CASCADE)
    house_number = models.ForeignKey(HouseNumber, on_delete=models.CASCADE)
    objects = models.Manager()


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    identity_number = models.PositiveIntegerField()
    post = models.ForeignKey(Position, on_delete=models.CASCADE)
    mobile_number = models.PositiveIntegerField()
    objects = models.Manager()


class StaffAttendance(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    time_in = models.DateTimeField(auto_now_add=True, editable=False)
    time_out = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StaffAttendanceReport(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(StaffAttendance, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffLeaveReport(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.DateField(auto_now_add=True)
    message = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class HomeOwnerNotification(models.Model):
    homeowner_id = models.ForeignKey(HomeOwner, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffNotification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class HomeOwnerFeedBack(models.Model):
    homeowner_id = models.ForeignKey(HomeOwner, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffFeedBack(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            HomeOwner.objects.create(admin=instance)
        if instance.user_type == 3:
            Staff.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.admin.save()
    if instance.user_type == 3:
        instance.admin.save()
