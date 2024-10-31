from django.shortcuts import render,get_object_or_404, redirect
from events.models import Activity, Sponsorship

def activity_list(request):
    activities = Activity.objects.all()
    sponsorships = Sponsorship.objects.all()
    context = {
        'activities': activities,
        'sponsorships': sponsorships
    }
    return render(request, 'events/event_list.html', context)

def toggle_activity_favorite(request, event_id):
    event = get_object_or_404(Activity, id=event_id)
    event.is_favorited = not event.is_favorited
    event.save()
    return redirect('activity_list')

# 用於贊助的收藏切換
def toggle_sponsorship_favorite(request, sponsorship_id):
    
    sponsorship = get_object_or_404(Sponsorship, id=sponsorship_id)
    sponsorship.is_favorited = not sponsorship.is_favorited
    sponsorship.save()
    return redirect('activity_list')



# Create your views here.
