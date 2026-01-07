from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your models here.

class OutfitPlan(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfits")
    date = models.DateField()
    title = models.TextField()
    mood = models.TextField()
    vibe = models.TextField()
    occasion = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="outfits/", blank=True, null=True)
    is_public = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date})"

class LookItem(models.Model):
    CATEGORY_CHOICES = [
        ("clothes", "Clothes"),
        ("shoes", "Shoes"),
        ("hair", "Hair"),
        ("makeup", "Makeup"),
        ("accessories", "Accessories"),
    ]

    outfit = models.ForeignKey(OutfitPlan, on_delete=models.CASCADE, related_name="looks")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="looks/", blank=True, null=True)
    notes = models.TextField(blank=True)

    where_to_buy = models.CharField(max_length=200, blank=True)
    product_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.outfit.title} - {self.category}"