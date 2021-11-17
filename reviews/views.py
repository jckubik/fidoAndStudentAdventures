from django.template.loader import render_to_string
from django.http import JsonResponse
from adventures.models import Review

# Create your views here.
# View to delete reviews
def delete(request):
    review_list = Review.objects.all()
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    review_id = request.POST.get('reviewId')
    location_id = request.POST.get('locationId')
    for review in review_list:
        if (review.id == review_id):
            break

    if is_ajax and request.method == 'POST':
        review_to_delete = Review.objects.get(pk=review_id)

        # Check authorization to delete the review
        if review_to_delete.author == request.session.get('username') or request.session.get('role') == 'admin':
            review_to_delete.delete()

            reviews = Review.objects.filter(adventureLocation__id=location_id).order_by('-date')

            # Render the review section as html to send as response
            htmlToRender = render_to_string(
                template_name='adventures/adventure_location/location_detail_review.html', context={'reviews': reviews}
            )
            data_dict = {'html_from_view': htmlToRender, 'success': 'success'}
            return JsonResponse(data=data_dict, safe=False, status=200)

        # Else, they're not authorized, do nothing
        else:
            data_dict = {'success': 'failure'}
            return JsonResponse(data=data_dict, status=200)

    else:
        return JsonResponse({'error': 'Invalid Ajax request.'}, status=400)