from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSection, Plant, About, CareTip, Video,
    ContactInfo, ContactMessage, Brochure, Article
)

# ---------------------------
# Helper for image/video preview
# ---------------------------
def plant_media_preview(obj):
    """Show video preview if available, else image preview"""
    if hasattr(obj, 'video') and obj.video:
        return format_html(
            '<video width="80" height="60" style="object-fit: cover;" autoplay loop muted playsinline>'
            '<source src="{}" type="video/mp4">'
            'Your browser does not support the video tag.'
            '</video>',
            obj.video.url
        )
    elif hasattr(obj, 'image') and obj.image:
        return format_html(
            '<img src="{}" style="width: 60px; height: 60px; object-fit: cover;" />',
            obj.image.url
        )
    return "No Media"

plant_media_preview.short_description = "Preview"

# ---------------------------
# Hero Section
# ---------------------------
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "cta_text")

# ---------------------------
# Plant / Catalog
# ---------------------------
@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name", "species", "price", "availability",
        "is_featured", plant_media_preview, "created_at"
    )
    list_filter = ("availability", "is_featured", "created_at")
    search_fields = ("name", "species")
    readonly_fields = ("created_at",)

# ---------------------------
# About
# ---------------------------
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("story",)

# ---------------------------
# Care Tips
# ---------------------------
@admin.register(CareTip)
class CareTipAdmin(admin.ModelAdmin):
    list_display = ("title", plant_media_preview, "created_at")
    search_fields = ("title",)
    readonly_fields = ("created_at",)

# ---------------------------
# Videos
# ---------------------------
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_type", "youtube_url", "created_at")
    list_filter = ("video_type", "created_at")
    search_fields = ("title",)
    readonly_fields = ("created_at",)

# ---------------------------
# Contact Info
# ---------------------------
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "address", "phone1", "phone2", "email",
        "facebook_url", "twitter_url", "youtube_url", "instagram_url"
    )

# ---------------------------
# Contact Messages
# ---------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at")
    search_fields = ("name", "email")
    readonly_fields = ("submitted_at",)

# ---------------------------
# Brochure PDF / Heyzine
# ---------------------------
@admin.register(Brochure)
class BrochureAdmin(admin.ModelAdmin):
    list_display = ("title", "pdf_file", "heyzine_link", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    list_editable = ("pdf_file", "heyzine_link")  # inline editing
    search_fields = ("title",)

# ---------------------------
# Article
# ---------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
