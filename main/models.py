"""
TODO:
1. FIX the eid field conditional check (generate/input manually)
2. Create the ID-CARD Model to record the amount of how many times did the employee assign an order to make the ID card
"""

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import random
from django.utils import timezone


def random_string():
    return str(random.randint(1, 10000))


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Sector(MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    # CHOICES
    BLOOD_TYPE_CHOICES = [
        ("o+", "O+"),
        ("o-", "O-"),
        ("a+", "A+"),
        ("a-", "A-"),
        ("b+", "B+"),
        ("b-", "B-"),
        ("ab+", "AB+"),
        ("ab-", "AB-"),
    ]
    # Employee Types Choices
    EMPLOYEE_TYPE_CHOICES = [("pns", "PNS"), ("p3k", "P3K"), ("honorer", "HONORER")]
    ECHELON_CHOICES = [
        ("2a", "IIA"),
        ("2b", "IIB"),
        ("3a", "IIIA"),
        ("3b", "IIIB"),
        ("4a", "IVA"),
        ("4b", "IVB"),
        ("5a", "VA"),
        ("5b", "VB"),
        ("non", "Non Eselon"),
        ("fungsional", "Fungsional"),
    ]
    CLASS_RANK_CHOICES = [
        ("1a", "IA"),
        ("1b", "IB"),
        ("1c", "IC"),
        ("1d", "ID"),
        ("2a", "IIA"),
        ("2b", "IIB"),
        ("2c", "IIC"),
        ("2d", "IID"),
        ("3a", "IIIA"),
        ("3b", "IIIB"),
        ("3c", "IIIC"),
        ("3d", "IIID"),
        ("4a", "IVA"),
        ("4b", "IVB"),
        ("4c", "IVC"),
        ("4d", "IVD"),
    ]

    # The Fields
    # FIXME Set the id of employee conditionally by checking the status of employee and whether it should generate random unique number id or manual input the id of employee has
    eid = models.CharField(
        max_length=30, unique=True, null=False, default=random_string, blank=False
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    birth_date = models.DateField()
    blood_type = models.CharField(
        max_length=3, choices=BLOOD_TYPE_CHOICES, default="O+"
    )
    occupation = models.CharField(max_length=100)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    sector = models.OneToOneField(Sector, on_delete=models.CASCADE)
    e_type = models.CharField(
        max_length=9, choices=EMPLOYEE_TYPE_CHOICES, default="pns"
    )
    echelon = models.CharField(
        max_length=15, choices=ECHELON_CHOICES, default="2a", blank=True, null=True
    )
    class_rank = models.CharField(
        max_length=5, choices=CLASS_RANK_CHOICES, default="1a", blank=True, null=True
    )
    # The Properties
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Card(models.Model):
    # CHOICES
    CARD_STATUS_CHOICES = [("ct1", "Diproses"), ("ct2", "Diambil"), ("ct3", "Selesai")]
    
    # The Fields
    application_date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(default=timezone.now)
    information = models.TextField()
    c_status = models.CharField(
        max_length=10, choices=CARD_STATUS_CHOICES, default="ct1"
    )
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="owner",default=None)
    taker = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="taker",blank=True,null=True)

