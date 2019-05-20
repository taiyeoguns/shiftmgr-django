const gulp = require("gulp");
const uglify = require("gulp-uglify");
const rename = require("gulp-rename");
const concat = require("gulp-concat");
const csso = require("gulp-csso");
const del = require("del");
const less = require("gulp-less");

gulp.task("clean", function() {
  del("static/*");
});

gulp.task("less", function() {
  return gulp
    .src("assets/less/shiftmgr.less")
    .pipe(less())
    .pipe(gulp.dest("assets/css"));
});

gulp.task("vendor-css", function() {
  return gulp
    .src([
      "node_modules/bootstrap/dist/css/bootstrap.min.css",
      "node_modules/font-awesome/css/font-awesome.min.css",
      "node_modules/ionicons/dist/css/ionicons.min.css"
    ])
    .pipe(concat("vendor.min.css"))
    .pipe(csso())
    .pipe(gulp.dest("static/css"));
});

gulp.task("app-css", ["less"], function() {
  return gulp
    .src([
      "node_modules/adminlte/dist/css/AdminLTE.css",
      "assets/css/shiftmgr.css",
      "assets/css/styles.css"
    ])
    .pipe(concat("app.min.css"))
    .pipe(csso())
    .pipe(gulp.dest("static/css"));
});

gulp.task("vendor-js", function() {
  return gulp
    .src([
      "node_modules/jquery/dist/jquery.min.js",
      "node_modules/bootstrap/dist/js/bootstrap.min.js"
    ])
    .pipe(concat("vendor.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("static/js"));
});

gulp.task("app-js", function() {
  return gulp
    .src([
      "node_modules/adminlte/dist/js/adminlte.min.js",
      "node_modules/initial-js/dist/initial.min.js",
      "assets/js/scripts.js"
    ])
    .pipe(concat("app.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("static/js"));
});

gulp.task("fonts", function() {
  return gulp
    .src([
      "node_modules/bootstrap/fonts/*",
      "node_modules/font-awesome/fonts/*",
      "node_modules/ionicons/dist/fonts/*"
    ])
    .pipe(gulp.dest("static/fonts"));
});

//app

gulp.task("shifts-index-css", function() {
  return gulp
    .src([
      "node_modules/datatables.net-bs/css/dataTables.bootstrap.min.css",
      "node_modules/chosen-js/chosen.min.css",
      "node_modules/bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css",
      "node_modules/jquery-confirm/dist/jquery-confirm.min.css"
    ])
    .pipe(concat("index.min.css"))
    .pipe(csso())
    .pipe(gulp.dest("static/css/shifts"));
});

gulp.task("shifts-css-images", function() {
  return gulp
    .src([
      "node_modules/chosen-js/chosen-sprite.png",
      "node_modules/chosen-js/chosen-sprite@2x.png"
    ])
    .pipe(gulp.dest("static/css/shifts"));
});

gulp.task("shifts-index-js", function() {
  return gulp
    .src([
      "node_modules/datatables.net/js/jquery.dataTables.min.js",
      "node_modules/datatables.net-bs/js/dataTables.bootstrap.min.js",
      "node_modules/moment/min/moment.min.js",
      "node_modules/datatable-sorting-datetime-moment/index.js",
      "node_modules/chosen-js/chosen.jquery.min.js",
      "node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js",
      "node_modules/jquery-confirm/dist/jquery-confirm.min.js",
      "node_modules/jquery-validation/dist/jquery.validate.min.js",
      "assets/js/ext/jquery.validate.bootstrap.js",
      "assets/js/shifts/index.js"
    ])
    .pipe(concat("index.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("static/js/shifts"));
});

//shifts-detail
gulp.task("shifts-detail-css", function() {
  return gulp
    .src([
      "node_modules/datatables.net-bs/css/dataTables.bootstrap.min.css",
      "node_modules/chosen-js/chosen.min.css",
      "node_modules/vis/dist/vis.min.css",
      "node_modules/jquery-ui/themes/base/datepicker.css",
      "node_modules/jquery-confirm/dist/jquery-confirm.min.css",
      "node_modules/jqueryui-timepicker-addon/dist/jquery-ui-timepicker-addon.min.css"
    ])
    .pipe(concat("detail.min.css"))
    .pipe(csso())
    .pipe(gulp.dest("static/css/shifts"));
});

gulp.task("shifts-detail-js", function() {
  return gulp
    .src([
      "node_modules/datatables.net/js/jquery.dataTables.min.js",
      "node_modules/datatables.net-bs/js/dataTables.bootstrap.min.js",
      "node_modules/moment/min/moment.min.js",
      "node_modules/datatable-sorting-datetime-moment/index.js",
      "node_modules/chosen-js/chosen.jquery.min.js",
      "node_modules/vis/dist/vis.min.js",
      "node_modules/jqueryui-timepicker-addon/dist/jquery-ui-timepicker-addon.min.js",
      "node_modules/jquery-confirm/dist/jquery-confirm.min.js",
      "node_modules/lodash/lodash.min.js",
      "node_modules/jquery-validation/dist/jquery.validate.min.js",
      "assets/js/ext/jquery.validate.bootstrap.js",
      "assets/js/shifts/detail.js"
    ])
    .pipe(concat("detail.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("static/js/shifts"));
});

//----//
gulp.task("default", [
  "clean",
  "less",
  "vendor-css",
  "app-css",
  "vendor-js",
  "app-js",
  "fonts",
  "shifts-css-images",
  "shifts-index-css",
  "shifts-index-js",
  "shifts-detail-css",
  "shifts-detail-js"
]);
