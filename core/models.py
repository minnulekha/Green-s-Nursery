from django.db import models

# ---------------------------
# 1. Hero Section
# ---------------------------
class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    banner_image = models.ImageField(upload_to="hero/")
    cta_text = models.CharField(max_length=50, default="Visit Us")
    cta_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

# ---------------------------
# 2. Plant / Catalog
# ---------------------------
class Plant(models.Model):
    AVAILABILITY_CHOICES = [
        ("Available", "Available"),
        ("Out", "Out of Stock"),
        ("Coming", "Coming Soon"),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default="Available")

    # Make image optional (used on other pages)
    image = models.ImageField(upload_to="plants/", blank=True, null=True)

    # New: optional video field for featured plants (mp4 recommended)
    video = models.FileField(upload_to="plants/videos/", blank=True, null=True,
                             help_text="Upload MP4 (H.264) for best compatibility")

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def has_video(self):
        return bool(self.video)

# ---------------------------
# 3. About Us
# ---------------------------
class About(models.Model):
    story = models.TextField()
    mission = models.TextField(blank=True)
    image = models.ImageField(upload_to="about/", blank=True)

    def __str__(self):
        return "About Section"

# ---------------------------
# 4. Care Tips
# ---------------------------
class CareTip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="caretips/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------------------------
# 5. Videos
# ---------------------------
class Video(models.Model):
    VIDEO_TYPES = [
        ("intro", "Intro Video"),
        ("regular", "Regular Video"),
        ("short", "Short / Reel"),
    ]

    title = models.CharField(max_length=200)
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES)
    youtube_url = models.URLField("YouTube URL", blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.video_type})"
    


# ---------------------------
# 6. Contact Info
# ---------------------------
class ContactInfo(models.Model):
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    delivery_note = models.TextField(default="Delivery available on call 📦")
    map_embed_link = models.TextField(blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    def __str__(self):
        return "Contact Info"

# ---------------------------
# 7. Contact Messages
# ---------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

# ---------------------------
# 8. Brochure PDF / Heyzine Link
# ---------------------------
class Brochure(models.Model):
    title = models.CharField(max_length=200)  # kept for admin/reference
    pdf_file = models.FileField(upload_to="brochures/", blank=True, null=True)  # PDF optional
    description = models.TextField(blank=True)
    heyzine_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Embed link for Heyzine flipbook"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------------------
# 9. Article
# ---------------------------
class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='articles/pdfs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
