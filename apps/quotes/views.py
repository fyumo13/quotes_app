from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from .models import Quote, Liker
from ..login_registration.models import User
import types

# displays login and registration page
def index(request):
    return render(request, 'login_registration/index.html')

# displays dashboard displaying all quotes posted by users and a favorites section
# containing quotes liked by the current user
# also contains a form to post a quote
def quotes(request):
    context = {
        'quotes': Quote.objects.all().exclude(liked_by=request.session['user_id']).order_by('-created_at'),
        'favorites': Quote.objects.filter(liked_by=request.session['user_id'])
    }
    return render(request, 'quotes/dashboard.html', context)

# allows user to post a quote with valid input
def post_quote(request):
    if request.method != 'POST':
        return redirect(reverse('quotes:quotes'))
    else:
        quote = Quote.objects.post_quote(request.POST, request.session['user_id'])
        if isinstance(quote, types.ListType):
            for error in quote:
                messages.error(request, error)
        return redirect(reverse('quotes:quotes'))

# displays a user-specific page containing all quotes posted by said user
def user(request, id):
    user = User.objects.annotate(num_posts=Count('poster')).get(id=id)
    context = {
        'user': user,
        'quotes': Quote.objects.filter(posted_by=user)
    }
    return render(request, 'quotes/user.html', context)

# allows user to add a specific quote to their list of favorites
def add_to_list(request, id):
    Quote.objects.add_to_list(id, request.session['user_id'], request.session['first_name'], request.session['last_name'])
    return redirect(reverse('quotes:quotes'))

# allows user to remove a specific quote from their list of favorites
def remove(request, id):
    Liker.objects.get(quote=id, user=request.session['user_id']).delete()
    return redirect(reverse('quotes:quotes'))
