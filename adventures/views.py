from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from .models import AdventureLocation, AdventureTrip, Review, User
from actions.models import Action
from django.http import JsonResponse
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractSummaryAction
)
import requests

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


# List view for trips
def adventure_trip_list(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    queryString = request.GET.get('queryString')


    if queryString:
        adventure_trips = AdventureTrip.objects.all().filter(name__icontains=queryString)

    # Else, default to order by name ascending
    else:
        adventure_trips = AdventureTrip.objects.all().order_by("-date")

    if is_ajax:
        if request.method == 'GET':

            # if ajax, then render the locations section to html with new ordered locations
            htmlToRender = render_to_string(
                template_name='adventures/adventure_location/trips_results.html',
                context={'adventure_trips': adventure_trips},
            )
            data_dict = {'html_from_view': htmlToRender, 'success': 'success'}
            return JsonResponse(data=data_dict, safe=False, status=200)

        else:
            return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)


    return render(request, 'adventures/adventure_location/list_trips.html', {'adventure_trips': adventure_trips})


# View for detail view
def adventure_location_detail(request, location_id):
    locations_list = AdventureLocation.objects.all()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    for location in locations_list:
        if (location.id == location_id):
            break

    reviews = Review.objects.filter(adventureLocation__id=location.id).order_by('-date')
    trips = AdventureTrip.objects.filter(adventureLocation__id=location.id).order_by('-date')

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

            # Update location review count
            location.num_reviews = location.num_reviews + 1
            location.save()


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
                      'adventure_trips': trips,
                      'reviews': reviews,
                  },
                  )


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


# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=ta_credential)
    return text_analytics_client


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

        # Check the data - content moderation
        endpoint = 'https://cs5774lang.cognitiveservices.azure.com/'
        key = '238baa4bb2154b73854657d97d4f244a'

        # Authenticate the client using your key and endpoint
        def authenticate_client():
            ta_credential = AzureKeyCredential(key)
            text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint,
                credential=ta_credential)
            return text_analytics_client

        client = authenticate_client()

        # document to analyze
        document = [description]

        # analyze the data
        poller = client.begin_analyze_actions(
            document,
            actions=[
                ExtractSummaryAction(MaxSentenceCount=2)
            ],
        )

        # Make result into a summary
        document_results = poller.result()
        for result in document_results:
            extract_summary_result = result[0]  # first document, first result
            if extract_summary_result.is_error:
                print("...Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
            else:
                response = " ".join([sentence.text for sentence in extract_summary_result.sentences])

        user = User.objects.get(username=request.session.get('username'))

        al = AdventureLocation(
            name=name,
            description=description,
            author=request.session.get('username'),
            user=user,
            img=main_image,
            alt=alt,
            summary=response,
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

# View for adding trip
def trip_creator(request, location_id):
    # Redirect if not logged in
    if not request.session.get('username', False):
        return redirect('adventures:home')

    location = AdventureLocation.objects.get(id=location_id)

    if request.method == 'POST':
        # Process the form
        date = request.POST.get('date')
        name = request.POST.get('tripName')
        description = request.POST.get('tripDescription')

        # Check the data - content moderation
        endpoint = 'https://cs5774lang.cognitiveservices.azure.com/'
        key = '238baa4bb2154b73854657d97d4f244a'

        # Authenticate the client using your key and endpoint
        def authenticate_client():
            ta_credential = AzureKeyCredential(key)
            text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint,
                credential=ta_credential)
            return text_analytics_client

        client = authenticate_client()

        # document to analyze
        document = [description]

        # analyze the data
        poller = client.begin_analyze_actions(
            document,
            actions=[
                ExtractSummaryAction(MaxSentenceCount=2)
            ],
        )

        # Make result into a summary
        document_results = poller.result()
        for result in document_results:
            extract_summary_result = result[0]  # first document, first result
            if extract_summary_result.is_error:
                print("...Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
            else:
                response = " ".join([sentence.text for sentence in extract_summary_result.sentences])

        user = User.objects.get(username=request.session.get('username'))

        # Add and save the trip
        at = AdventureTrip(
            name=name,
            description=description,
            author=request.session.get('username'),
            adventureLocation=location,
            user=user,
            summary=response,
        )
        at.save()

        # Log the action
        action = Action(
            user=user,
            verb="created a new trip:",
            target=at,
        )
        action.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            "You successfully created a new trip: %s" % at.name,
        )
        return redirect('adventures:adventure_location_detail', location.id)

    else:
        # show the form
        return render(request,
                      'adventures/adventure_location/creator_trips.html',
                      {'location': location},
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

# View for about page
def about(request):
    return render(
        request,
        'adventures/adventure_location/about.html',
    )

# View for Contact page
def contact(request):
    return render(
        request,
        'adventures/adventure_location/contact.html',
    )

# View for Help page
def help(request):
    return render(
        request,
        'adventures/adventure_location/help.html',
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