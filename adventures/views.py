from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from .models import AdventureLocation, AdventureTrip, Review, User
from actions.models import Action
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def adventure_location_list(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    orderType = request.GET.get('orderType')
    queryString = request.GET.get('queryString')

    #if orderType exists, then create new ordered querySet
    if orderType:
        adventure_locations = AdventureLocation.objects.all().order_by(orderType)

    elif queryString:
        adventure_locations = AdventureLocation.objects.all().filter(name__icontains=queryString)

    # Else, default to order by name ascending
    else:
        adventure_locations = AdventureLocation.objects.all().order_by("name")

    if is_ajax:
        if request.method == 'GET':

            # if ajax, then render the locations section to html with new ordered locations
            htmlToRender = render_to_string(
                template_name='adventures/adventure_location/locations_results.html', context={'adventure_locations': adventure_locations}
            )
            data_dict = {'html_from_view': htmlToRender, 'success': 'success'}
            return JsonResponse(data=data_dict, safe=False, status=200)

        else:
            return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


    return render(request, 'adventures/adventure_location/list.html', {'adventure_locations': adventure_locations})

# View for detail view
def adventure_location_detail(request, location_id):
    locations_list = AdventureLocation.objects.all()
    adventure_trips = AdventureTrip.objects.all()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    for location in locations_list:
        if (location.id == location_id):
            break

    reviews = Review.objects.filter(adventureLocation__id=location.id).order_by('-date')

    if is_ajax:
        if request.method == 'POST':

            adventureId = request.POST.get('adventureId')
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            theAdventure = AdventureLocation.objects.get(pk=adventureId)

            # Create a new Review object and add to DB
            nr = Review(
                adventureLocation=theAdventure,
                author=request.session.get('username'),
                review=review,
                rating=rating,
            )
            nr.save()


            # Log the action
            user = User.objects.get(username=request.session.get('username'))
            action = Action(
                user=user,
                verb="left a new review on:",
                target=theAdventure,
            )
            action.save()

            # Render the review section as html to send as response
            htmlToRender = render_to_string(
                template_name='adventures/adventure_location/location_detail_review.html', context={'reviews': reviews}
            )
            data_dict = {'html_from_view': htmlToRender, 'success': 'success'}
            return JsonResponse(data=data_dict, safe=False, status=200)

        else:
            return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)

    return render(request,
                  'adventures/adventure_location/detail.html',
                  {
                      'location': location,
                      'adventure_trips': adventure_trips,
                      'reviews': reviews,
                  },
                  )


# View to delete reviews
def delete_review(request):
    review_list = Review.objects.all()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    review_id = request.POST.get('reviewId')
    location_id = request.POST.get('locationId')
    reviews = Review.objects.filter(adventureLocation__id=location_id).order_by('-date')
    for review in review_list:
        if (review.id == review_id):
            break

    if is_ajax and request.method == 'POST':
            review_to_delete = Review.objects.get(pk=review_id)
            review_to_delete.delete()

            # Render the review section as html to send as response
            htmlToRender = render_to_string(
                template_name='adventures/adventure_location/location_detail_review.html', context={'reviews': reviews}
            )
            data_dict = {'html_from_view': htmlToRender, 'success': 'success'}
            return JsonResponse(data=data_dict, safe=False, status=200)

    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


# View for search function
def adventure_location_search(request):
    return render(request,
                  'adventures/adventure_location/search.html',
                  )


# View for results page
def adventure_search_results(request):
    return render(request,
                  'adventures/adventure_location/search_results.html',
                  )


# View for adding location
def adventure_creator(request):
    # Redirect if not logged in
    if not request.session.get('username', False):
        return redirect('adventures:home')

    if request.method == 'POST':
        # Process the form
        main_image = request.POST.get('locationMainImage')
        name = request.POST.get('locationName')
        description = request.POST.get('locationDescription')
        alt = request.POST.get('mainImageAlt')

        user = User.objects.get(username=request.session.get('username'))

        al = AdventureLocation(
            name=name,
            description=description,
            author=request.session.get('username'),
            user=user,
            img=main_image,
            alt=alt,
        )
        al.save()

        # Log the action
        action = Action(
            user=user,
            verb="created the adventure location:",
            target=al,
        )
        action.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "You successfully created a new location: %s" % al.name,
        )
        return redirect('adventures:adventure_location_detail', al.id)

    else:
        # show the form
        return render(request,
                      'adventures/adventure_location/creator.html',
                      )


# View for home page
def home(request):
    locations_list = AdventureLocation.objects.all()
    adventure_trips = AdventureTrip.objects.all()

    if request.session.get('username', False):
        # Logged in
        actions = Action.objects.all().order_by('-created')


        return render(request,
                  'adventures/adventure_location/home.html',
                  {'adventure_locations': locations_list,
                   'adventure_trips': adventure_trips,
                   'actions': actions,
                   },
                  )

    else:
        return render(request,
                  'adventures/adventure_location/home_logged_out.html',
                  {'adventure_locations': locations_list,
                   'adventure_trips': adventure_trips,
                   },
                  )

# View to edit location
def edit_location(request, location_id):
    # Redirect if not logged in
    if not request.session.get('username', False):
        return redirect('adventures:home')

    if request.method == 'POST':
        # Process the form
        adventure = AdventureLocation.objects.get(pk=location_id)
        adventure.name = request.POST.get('locationName')
        adventure.description = request.POST.get('locationDescription')
        adventure.img = request.POST.get('locationMainImage')
        adventure.alt = request.POST.get('mainImageAlt')
        adventure.save()
        user = User.objects.get(username=request.session.get('username'))

        # Log the action
        action = Action(
            user=user,
            verb="edited a location:",
            target=adventure,
        )
        action.save()

        messages.add_message(
            request,
            messages.INFO,
            "You successfully updated location: %s" % adventure.name,
        )
        return redirect('adventures:adventure_location_detail', location_id)

    # Load the form with existing data
    else:
        locations_list = AdventureLocation.objects.all()
        adventure_trips = AdventureTrip.objects.all()
        for location in locations_list:
            if (location.id == location_id):
                break
        return render(request,
                      'adventures/adventure_location/edit.html',
                      {
                          'location': location,
                          'adventure_trips': adventure_trips,
                      },
                      )

# View to delete location
def delete_location(request, location_id):
    location_id = request.POST.get('locationId')
    adventure = AdventureLocation.objects.get(pk=location_id)
    name = adventure.name
    adventure.delete()
    user = User.objects.get(username=request.session.get('username'))

    # Log the action
    action = Action(
        user=user,
        verb="deleted a location",
    )
    action.save()

    messages.add_message(
        request,
        messages.WARNING,
        "Location %s successfully deleted" % name,
    )
    return redirect('adventures:adventure_location_list')