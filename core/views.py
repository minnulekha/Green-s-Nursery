from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.http import JsonResponse
from .models import (
    HeroSection,
    Plant,
    About,
    CareTip,
    Video,
    ContactInfo,
    Brochure,
    ContactMessage,
    Article
)
from datetime import datetime
from urllib.parse import urlparse, parse_qs


# =========================================
# Helper Functions
# =========================================

def generate_embed_url(youtube_url, start=None, end=None, autoplay=False, loop=False):
    """
    Generate a YouTube embed URL with optional autoplay, loop, and start/end times.
    """
    if not youtube_url:
        return None

    parsed_url = urlparse(youtube_url)
    video_id = None

    # Detect YouTube video ID
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            query = parse_qs(parsed_url.query)
            video_id = query.get("v", [None])[0]
        elif parsed_url.path.startswith("/shorts/"):
            parts = parsed_url.path.split("/")
            if len(parts) > 2:
                video_id = parts[2]
    elif parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.lstrip("/")

    if not video_id:
        return None

    # Build query params
    params = []
    if autoplay:
        params.append("autoplay=1")
        params.append("mute=1")
    if loop:
        params.append("loop=1")
        params.append(f"playlist={video_id}")
    if start:
        params.append(f"start={start}")
    if end:
        params.append(f"end={end}")

    query_string = "&".join(params)
    return (
        f"https://www.youtube.com/embed/{video_id}?{query_string}"
        if query_string
        else f"https://www.youtube.com/embed/{video_id}"
    )


def extract_video_id(youtube_url):
    """
    Extract YouTube video ID from a given URL.
    """
    if not youtube_url:
        return None

    parsed = urlparse(youtube_url)
    hostname = parsed.hostname or ""

    if "youtube.com" in hostname:
        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            return qs.get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            parts = parsed.path.split("/")
            if len(parts) >= 3:
                return parts[2]

    if "youtu.be" in hostname:
        return parsed.path.lstrip("/")

    return None


# =========================================
# Homepage View
# =========================================
def home(request):
    if request.method == "POST":
        # Contact form submission
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=f"{subject}\n\n{message}" if subject else message,
            )
        return redirect("home")

    # ----------------------------
    # Hero Section
    # ----------------------------
    hero = HeroSection.objects.first()

    # ----------------------------
    # Featured Plants (Image or Video)
    # ----------------------------
    plants = Plant.objects.filter(is_featured=True)[:6]
    for plant in plants:
        if plant.video:  
            # Uploaded MP4 video
            plant.embed_video_url = plant.video.url
            plant.is_youtube = False
        elif hasattr(plant, "youtube_url") and plant.youtube_url:
            # Optional YouTube link
            plant.embed_video_url = generate_embed_url(plant.youtube_url, autoplay=True, loop=True)
            plant.is_youtube = True
        else:
            plant.embed_video_url = None
            plant.is_youtube = False

    # ----------------------------
    # About Section
    # ----------------------------
    about = About.objects.first()

    # ----------------------------
    # Care Tips Section
    # ----------------------------
    care_tips = CareTip.objects.all()[:3]

    # ----------------------------
    # Videos Section
    # ----------------------------
    videos = Video.objects.all().order_by("-id")

    # Intro Video
    intro_video = videos.filter(video_type="intro").first()
    if intro_video and intro_video.youtube_url:
        intro_video.embed_url = generate_embed_url(
            intro_video.youtube_url,
            start=80,
            end=160,
            autoplay=True
        )

    # Regular Videos
    other_videos = videos.filter(video_type="regular")
    if intro_video:
        other_videos = other_videos.exclude(id=intro_video.id)

    for video in other_videos:
        if video.youtube_url:
            video.embed_url = generate_embed_url(video.youtube_url)

    # Latest Short Video
    latest_short = videos.filter(video_type="short").order_by("-created_at", "-id").first()
    if latest_short and latest_short.youtube_url:
        vid = extract_video_id(latest_short.youtube_url)
        if vid:
            latest_short.embed_url = generate_embed_url(latest_short.youtube_url, autoplay=True, loop=True)
            latest_short.thumb_url = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

    # ----------------------------
    # Brochure
    # ----------------------------
    brochure = Brochure.objects.first()

    # ----------------------------
    # Contact Info
    # ----------------------------
    contact_info = ContactInfo.objects.first()

    # ----------------------------
    # Articles
    # ----------------------------
    articles = Article.objects.all()

    # ----------------------------
    # Final Context
    # ----------------------------
    context = {
        "hero": hero,
        "plants": plants,
        "about": about,
        "care_tips": care_tips,
        "intro_video": intro_video,
        "other_videos": other_videos,
        "latest_short": latest_short,
        "brochure": brochure,
        "contact_info": contact_info,
        "articles": articles,
        "current_year": datetime.now().year,
    }

    return render(request, "core/home.html", context)


# =========================================
# Shorts Page
# =========================================

def shorts_view(request):
    videos = Video.objects.filter(video_type="short").order_by("-created_at", "-id")
    short_videos = []
    for video in videos:
        if not video.youtube_url:
            continue
        vid = extract_video_id(video.youtube_url)
        if not vid:
            continue
        video.embed_url = generate_embed_url(video.youtube_url, loop=True)
        video.thumb_url = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        short_videos.append(video)

    contact_info = ContactInfo.objects.first()
    return render(request, "core/shorts.html", {"short_videos": short_videos, "contact_info": contact_info})


# =========================================
# All Regular Videos
# =========================================

def all_videos_view(request):
    videos = Video.objects.filter(video_type="regular").order_by("-created_at", "-id")
    for video in videos:
        if video.youtube_url:
            video.embed_url = generate_embed_url(video.youtube_url)

    contact_info = ContactInfo.objects.first()
    return render(request, "core/all_videos.html", {"videos": videos, "contact_info": contact_info})


# =========================================
# Plant Autocomplete & List
# =========================================

def plant_autocomplete(request):
    term = request.GET.get("term", "")
    results = []
    if term:
        matches = Plant.objects.filter(name__istartswith=term)[:10]
        results = list(matches.values_list("name", flat=True))
    return JsonResponse(results, safe=False)


def plants_list(request):
    query = request.GET.get("q")
    plants = Plant.objects.all()
    contact_info = ContactInfo.objects.first()

    if query:
        # Search with direct match
        candidates = plants.filter(
            Q(name__icontains=query) |
            Q(species__icontains=query) |
            Q(description__icontains=query)
        )

        # If no direct matches, use fuzzy matching
        if not candidates.exists():
            best_matches = [
                plant.id
                for plant in plants
                if fuzz.partial_ratio(query.lower(), plant.name.lower()) > 60
            ]
            candidates = plants.filter(id__in=best_matches)

        plants = candidates

    # Pre-generate embed URLs for plants with video URLs
    for plant in plants:
        if hasattr(plant, "video_url") and plant.video_url:
            plant.embed_url = generate_embed_url(plant.video_url, autoplay=True, loop=True)
        else:
            plant.embed_url = None

    return render(request, "core/plants.html", {
        "plants": plants,
        "contact_info": contact_info
    })
