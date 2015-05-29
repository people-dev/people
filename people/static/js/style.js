$('.ui.dropdown')
  .dropdown()
;
$('.message .close').on('click', function() {
  $(this).closest('.message').fadeOut();
});
$('.ui.sticky')
  .sticky({
    context: '#context'
  })
;