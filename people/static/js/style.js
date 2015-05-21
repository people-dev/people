$('.ui.dropdown')
  .dropdown()
;
$('.message .close').on('click', function() {
  $(this).closest('.message').fadeOut();
});