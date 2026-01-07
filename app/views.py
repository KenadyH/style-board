from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OutfitPlanForm, LookItemForm
from .models import OutfitPlan
from datetime import date, timedelta
from django.utils.dateparse import parse_date
# Create your views here.
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "registration/register.html", {"form": form})

@login_required
def home(request):
    plans = OutfitPlan.objects.filter(user=request.user).order_by("date")
    return render(request, "home.html", {"plans": plans})

def _monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())


@login_required
def create_outfit_plan(request):
    if request.method == "POST":
        form = OutfitPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect("home")
    else:
        form = OutfitPlanForm()

    return render(request, "outfits/create_plan.html", {"form": form})


@login_required
def week_view(request):
    start_str = request.GET.get("start")
    start = parse_date(start_str) if start_str else None

    today = date.today()
    monday = _monday_of_week(start or today)

    week_days = [monday + timedelta(days=i) for i in range(7)]

    plan_qs = OutfitPlan.objects.filter(
        user=request.user,
        date__range=(week_days[0], week_days[-1]),
    )

    plans_by_date = {p.date: p for p in plan_qs}

    rows = []
    for d in week_days:
        rows.append({
            "date": d,
            "plan": plans_by_date.get(d),
        })

    prev_monday = monday - timedelta(days=7)
    next_monday = monday + timedelta(days=7)

    return render(request, "week.html", {
        "monday": monday,
        "rows": rows,
        "prev_start": prev_monday.isoformat(),
        "next_start": next_monday.isoformat(),
    })

def public_feed(request):
    plans = OutfitPlan.objects.filter(is_public=True).select_related("user").order_by("-date")
    return render(
        request,
        "outfits/public_feed.html",
        {"plans": plans}
    )

def public_outfit_detail(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, is_public=True)
    return render(request, "outfits/public_detail.html", {"plan": plan})


@login_required
def plan_this_week(request):
    today = date.today()
    monday = _monday_of_week(today)

    for i in range(7):
        d = monday + timedelta(days=i)
        OutfitPlan.objects.get_or_create(
            user=request.user,
            date=d,
            defaults={
                "title": f"Outfit for {d.strftime('%A')}",
                "mood": "",
                "occasion": "",
            },
        )
        return redirect("week_view")


    messages.success(request, "Your week has been created/updated ")
    return redirect("home")


@login_required
def outfit_detail(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, user=request.user)
    items = plan.looks.all().order_by("category", "-created_at")

    grouped = {}
    for item in items:
        grouped.setdefault(item.category, []).append(item)

    return render(request, "outfits/detail.html", {
        "plan": plan,
        "grouped": grouped,
    })

@login_required
def edit_outfit_plan(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, user=request.user)

    if request.method == "POST":
        form = OutfitPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = OutfitPlanForm(instance=plan)

    return render(request, "outfits/edit_plan.html", {"form": form, "plan": plan})

@login_required
def delete_outfit_plan(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, user=request.user)

    if request.method == "POST":
        plan.delete()
        return redirect("home")

    return render(request, "outfits/delete_plan.html", {"plan": plan})


@login_required
def add_look_item(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, user=request.user)

    if request.method == "POST":
        form = LookItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.outfit = plan
            item.save()
            return redirect("outfit_detail", plan_id=plan.id)
    else:
        form = LookItemForm()

    return render(request, "outfits/add_item.html", {"form": form, "plan": plan})

@login_required
def admin_delete_any_outfit(request, plan_id):
    if not request.user.is_staff:
        return redirect("public_feed")

    plan = get_object_or_404(OutfitPlan, id=plan_id)
    if request.method == "POST":
        plan.delete()
        return redirect("public_feed")

    return render(request, "outfits/admin_delete_any.html", {"plan": plan})

@login_required
def public_feed(request):
    plans = OutfitPlan.objects.filter(is_public=True).select_related("user").order_by("-date")
    return render(request, "outfits/public_feed.html", {"plans": plans})


@login_required
def public_outfit_detail(request, plan_id):
    plan = get_object_or_404(OutfitPlan, id=plan_id, is_public=True)
    return render(request, "outfits/public_detail.html", {"plan": plan})