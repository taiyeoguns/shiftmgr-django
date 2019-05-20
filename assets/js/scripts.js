//Scripts

//use initials as avatar
$(".avatar").initial();

//close alert after some time
$(".alert")
  .not(".alert-important")
  .delay(4000)
  .slideUp(200, function() {
    $(this).alert("close");
  });
