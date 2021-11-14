// .ready() only runs once the page is finished loading
$(document).ready(function() {

  // Functionality for clicking the favorite button ------------------

  // For locationPage.html icon
  $("#location-page-heartIcon").on("click", handleFavoriteButton);

  // For all heartIcons besides on locationPage.html
  $("article").on("click", "img.heartIcon", handleFavoriteButton);

  // Function to handle the click
  function handleFavoriteButton() {

    // Check which img to display
    let image;
    let favoritedMessage;

    if (this.src.indexOf("Clicked") !== -1) {
      image = "/static/media/heart.svg";
    } else {
      image = "/static/media/heartClicked.svg";
      favoritedMessage = $('<p class="favoritedMsg">Favorited!</p>');
    }

    // Display it
    $(this).attr("src", image);


    // Show and remove "Favorited!" div
    $(favoritedMessage).appendTo( $(this).parent() ).fadeOut('slow', function() {
      $(this).remove();
    });
  }

  // Delete Location Confirmation
  $('#deleteLocationButton').on('click', function() {
    return confirm("Are you sure?");
  });

  // Submit Ajax request to order locations ----------------------
  // Function to submit form on section tag change
  $('#listViewSortByList').on('change', function() { return $(this).parent().submit()})

  // Listen for submit and send via Ajax instead
  $('#listViewSortByForm').on('submit', function(event) {
    event.preventDefault();
    const orderType = $('#listViewSortByList').val();
    const ajaxURL = $('#listViewSortByList').attr('data-ajax-url');

    // Using the core $.ajax() method
    $.ajax({

      // The URL for the request
      url: ajaxURL,

      // The data to send (will be converted to a query string)
      data: {
          orderType: orderType,
      },

      // Whether this is a POST or GET request
      type: "GET",

      // The type of data we expect back
      dataType : "json",

      // The CSRF token to be passed
      headers: {'X-CSRFToken': csrftoken},
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function( json ) {
      // alert("request received successfully");
      if (json.success == 'success') {

          // If success, then render the locations-results template with the ordered queryset
          $('#results').html(json['html_from_view']);
      } else {
          alert('Error: ' + json.error);
      }
    })
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
      console.log( "Error: " + errorThrown );
    })
    // Code to run regardless of success or failure;
    .always(function( xhr, status ) {
    });
  });

  // Add a review to a specific adventure--------------
     $('#detailViewReviewForm').on('submit', function(event) {
         event.preventDefault();
         const ajaxURL = $('#detailViewReviewForm').attr('data-ajax-url');
         const author = $('#author').val();
         const adventureId = $('#adventureId').val();
         const review = $('#review').val();
         const rating = $('#detailViewRating').val();

         // Using the core $.ajax() method
        $.ajax({

          // The URL for the request
          url: ajaxURL,

          // The data to send (will be converted to a query string)
          data: {
              author: author,
              adventureId: adventureId,
              review: review,
              rating: rating,
          },

          // Whether this is a POST or GET request
          type: "POST",

          // The type of data we expect back
          dataType : "json",

          // The CSRF token to be passed
          headers: {'X-CSRFToken': csrftoken},
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
          if (json.success == 'success') {
              // If success, then render the locations-results template with the ordered queryset
              $('#review-user').html(json['html_from_view']);
          } else {
              alert('Error: ' + json.error);
          }
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
          console.log( "Error: " + errorThrown );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        });
     });

     // Search the locations by name ---------------------
    $('#search').on('submit', function(event) {
         event.preventDefault();
         const ajaxURL = $('#detailViewReviewForm').attr('data-ajax-url');
         const queryString = $('#searchQueryString').val();


         // Using the core $.ajax() method
        $.ajax({

          // The URL for the request
          url: ajaxURL,

          // The data to send (will be converted to a query string)
          data: {
                queryString: queryString,
          },

          // Whether this is a POST or GET request
          type: "GET",

          // The type of data we expect back
          dataType : "json",

          // The CSRF token to be passed
          headers: {'X-CSRFToken': csrftoken},
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
          if (json.success == 'success') {
            console.log('success triggered');
              // If success, then render the locations-results template with the ordered queryset
              $('#results').html(json['html_from_view']);
          } else {
              alert('Error: ' + json.error);
          }
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
        });
     });

}); // End of ready function

// Gets the CSRF token for Ajax requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
