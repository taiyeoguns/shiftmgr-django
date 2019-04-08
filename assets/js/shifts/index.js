$(function() {
  $(".table tbody tr")
    .hover(function() {
      $(this).css("cursor", "pointer");
    })
    .click(function(e) {
      if ($(e.target).is("td")) window.location.href = $(this).attr("href");
    });

  /**/
  $.fn.dataTable.moment("DD/MM/YYYY");
  $(".shifts-table").DataTable();
  $(".past-shifts-table").DataTable({
    order: [[0, "desc"]]
  });
  /**/

  //datepicker
  $("#shift_date").datepicker({
    format: "dd/mm/yyyy",
    startDate: "today",
    daysOfWeekHighlighted: "1,2,3,4,5",
    daysOfWeekDisabled: "0,6",
    calendarWeeks: true,
    autoclose: true,
    todayHighlight: true
  });

  //validate chosen select
  $.validator.setDefaults({ ignore: ":hidden:not(select)" });

  var validator = $("#shift-form").validate({
    errorPlacement: function(error, element) {
      if (element.attr("id") == "manager") {
        error.insertAfter("#manager_chosen");
      } else if (element.attr("id") == "members") {
        error.insertAfter("#members_chosen");
      } else {
        error.insertAfter(element);
      }
    },
    messages: {
      shift_date: "Choose the shift date",
      manager: "Select a manager"
    }
  });

  $("#modalSubmitBtn").click(function() {
    //call submit of the form directly
    $("#shift-form").submit();
  });

  $("#modal").on("hidden.bs.modal", function(e) {
    //reset form on close
    $("#shift-form").trigger("reset");
    $("#manager, #members")
      .val("")
      .trigger("chosen:updated");
    validator.resetForm();
  });

  $("#manager, #members").chosen({
    width: "100%"
  });
});
