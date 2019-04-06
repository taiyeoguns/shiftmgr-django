//Scripts

//use initials as avatar
$(".avatar").initial();

//close alert after some time
$(".alert")
  .delay(4000)
  .slideUp(200, function() {
    $(this).alert("close");
  });
