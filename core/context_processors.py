from django.core.cache import cache
from core.models import Activity

def activities_processor(request):
    """
    Expose cached activities list to all templates
    """
    # Try to get activities from cache
    activities = cache.get('navbar_activities')
    
    if activities is None:
        # If not in cache, get from database and cache for 1 hour
        activities = Activity.objects.filter(status='active').order_by('title')
        cache.set('navbar_activities', activities, 60 * 60)
    
    return {
        'activities': activities
    }