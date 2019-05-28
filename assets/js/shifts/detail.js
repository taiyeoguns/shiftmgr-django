is_member = JSON.parse($("#sm_is_member").text());
timeline_data = JSON.parse($("#sm_timeline_data").text());

var container = document.getElementById("timeline");
var items = new vis.DataSet(timeline_data);

if (!is_member) {
  var groups_data = JSON.parse($("#sm_groups_data").text());
  var groups = new vis.DataSet(groups_data);
}

var options = {
  showCurrentTime: true,
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
