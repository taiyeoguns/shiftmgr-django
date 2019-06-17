is_member = JSON.parse($("#sm_is_member").text());
timeline_data = JSON.parse($("#sm_timeline_data").text());
shift_date = JSON.parse($("#sm_shift_date").text());

var container = document.getElementById("timeline");
var items = new vis.DataSet(timeline_data);

if (!is_member) {
  var groups_data = JSON.parse($("#sm_groups_data").text());
  var groups = new vis.DataSet(groups_data);
}

var options = {
  showCurrentTime: true,
  min: moment(shift_date + " 08", "YYYY-MM-DD HH"),
  max: moment(shift_date + " 17", "YYYY-MM-DD HH"),
  dataAttributes: "all"
};

// initialize timeline
if (is_member) {
  var timeline = new vis.Timeline(container, items, options);
} else {
  var timeline = new vis.Timeline(container, items, groups, options);
}

/* timeline buttons*/

/**
 * Move the timeline a given percentage to left or right
 * @param {Number} percentage   For example 0.1 (left) or -0.1 (right)
 */
function move(percentage) {
  var range = timeline.getWindow();
  var interval = range.end - range.start;

  timeline.setWindow({
    start: range.start.valueOf() - interval * percentage,
    end: range.end.valueOf() - interval * percentage
  });
}

/**
 * Zoom the timeline a given percentage in or out
 * @param {Number} percentage   For example 0.1 (zoom out) or -0.1 (zoom in)
 */
function zoom(percentage) {
  var range = timeline.getWindow();
  var interval = range.end - range.start;

  timeline.setWindow({
    start: range.start.valueOf() - interval * percentage,
    end: range.end.valueOf() + interval * percentage
  });
}

// attach events to the navigation buttons
document.getElementById("zoomIn").onclick = function() {
  zoom(-0.2);
};
document.getElementById("zoomOut").onclick = function() {
  zoom(0.2);
};
document.getElementById("moveLeft").onclick = function() {
  move(0.2);
};
document.getElementById("moveRight").onclick = function() {
  move(-0.2);
};

//display message if timeline not available
if (!timeline_data || !timeline_data.length) {
  $("#timeline").html("<em>No timeline available</em>");
}

$.fn.dataTable.moment("hh:mm A");
tasks_table = $("#tasks-table").DataTable({
  pageLength: 10,
  lengthMenu: [5, 10, 20],
  language: {
    emptyTable: "No tasks logged"
  },
  order: [[is_member ? 1 : 2, "asc"]]
});

//

$("#end_block").hide();

$("#time_toggle").click(function() {
  $("#end").prop("disabled", false);
  if ($("#end_block").css("display") == "none") {
    $("#end_block").show();
    $(this)
      .removeClass("fa-plus")
      .addClass("fa-minus")
      .attr("title", "Remove Finish Time");
  } else {
    $("#end_block").hide();
    $(this)
      .removeClass("fa-minus")
      .addClass("fa-plus")
      .attr("title", "Add Finish Time");
  }
});

var start_options = {
  timeFormat: "hh:mm TT",
  ampm: true,
  hourMin: 8,
  hourMax: 16,
  showMillisec: false,
  showTimezone: false
};

if ($("#end").css("display") !== "none") {
  start_options.onClose = function(dateText, inst) {
    if ($("#end").val() != "") {
      var testStartTime = $("#start").datetimepicker("getDate");
      var testEndTime = $("#end").datetimepicker("getDate");
      if (testStartTime > testEndTime) {
        $("#end").timepicker("setDate", testStartTime);
      }
    } else {
      $("#end").val(dateText);
    }
  };

  start_options.onSelect = function(selectedDateTime) {
    var testStartTime = $("#start").datetimepicker("getDate");
    var testEndTime = $("#end").datetimepicker("getDate");

    if (testStartTime > testEndTime) {
      $("#end").datetimepicker(
        "option",
        "minDate",
        $("#start").datetimepicker("getDate")
      );
    }
  };
}

$("#start").timepicker(start_options);
$("#add_call_btn").click(function() {
  $("#start").timepicker("setDate", new Date());
});

$("#end").timepicker({
  timeFormat: "hh:mm TT",
  ampm: true,
  hourMin: 8,
  hourMax: 16,
  showMillisec: false,
  showTimezone: false,
  onClose: function(dateText, inst) {
    if ($("#start").val() != "") {
      var testStartTime = $("#start").datetimepicker("getDate");
      var testEndTime = $("#end").datetimepicker("getDate");
      if (testStartTime > testEndTime) {
        $("#start").timepicker("setDate", testEndTime);
      }
    } else {
      $("#start").val(dateText);
    }
  },
  onSelect: function(selectedDateTime) {
    var testStartTime = $("#start").datetimepicker("getDate");
    var testEndTime = $("#end").datetimepicker("getDate");

    if (testStartTime > testEndTime) {
      $("#start").datetimepicker(
        "option",
        "maxDate",
        $("#end").datetimepicker("getDate")
      );
    }
  }
});

//for chosen select
$.validator.setDefaults({ ignore: ":hidden:not(select)" });

//submit form
var validator = $("#task-form").validate({
  errorPlacement: function(error, element) {
    if (element.attr("id") == "member") {
      error.insertAfter("#member_chosen");
    } else if (element.attr("id") == "status") {
      error.insertAfter("#status_chosen");
    } else if (element.attr("id") == "priority") {
      error.insertAfter("#priority_chosen");
    } else {
      error.insertAfter(element);
    }
  },
  rules: {
    title: {
      maxlength: 24
    }
  },
  messages: {
    start: "Enter the time the task started",
    end: "Enter the time the task was finished",
    title: {
      required: "Add task title",
      maxlength: "Task title too long"
    }
  }
});

$("#modalSubmitBtn").click(function() {
  if ($("#end_block").css("display") == "none") {
    $("#end").prop("disabled", true);
  }

  //submit form
  $("#task-form").submit();
});

$("#modal").on("shown.bs.modal", function(e) {
  //focus on first field
  $("#task").focus();
});

$("#modal").on("hidden.bs.modal", function(e) {
  //reset form on close
  $("#task-form").trigger("reset");
  $("#member, #status, #priority")
    .val("")
    .trigger("chosen:updated");

  validator.resetForm();
});

$("#member").chosen({
  width: "100%",
  no_results_text: "No member matched"
});

$("#status").chosen({
  width: "100%",
  no_results_text: "Invalid status"
});

$("#priority").chosen({
  width: "100%",
  no_results_text: "Invalid priority"
});
