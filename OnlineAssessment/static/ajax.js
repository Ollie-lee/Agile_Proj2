$('.ajax-btn').click(function() {
  $('.res').text('loading . . .');
  
  $.ajax({
    type:"GET",
    url:"https://api.meetup.com/2/cities",
    success: function(data) {
      $('.res').text(JSON.stringify(data.results));
    },
    dataType: 'jsonp',
  });
  
});