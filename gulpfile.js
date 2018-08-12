const gulp = require('gulp');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');
const concat = require('gulp-concat');
const csso = require('gulp-csso');
const del = require('del');
const less = require('gulp-less');

gulp.task('clean', function(){
	del('static/*');
});

gulp.task('less', function(){
	return gulp.src('assets/less/shiftmgr.less')
	.pipe(less())
	.pipe(gulp.dest('assets/css'));
});

gulp.task('vendor-css', function(){
	return gulp.src([
		'node_modules/bootstrap/dist/css/bootstrap.min.css', 
		'node_modules/font-awesome/css/font-awesome.min.css',
		'node_modules/ionicons/dist/css/ionicons.min.css'
		])
	.pipe(concat('vendor.min.css'))
	.pipe(csso())
	.pipe(gulp.dest('static/css'));
});

gulp.task('app-css', ['less'], function(){
	return gulp.src([
		'node_modules/bootstrap/dist/css/bootstrap.min.css', 
		'node_modules/adminlte/dist/css/AdminLTE.css',
		'assets/css/shiftmgr.css',
		'assets/css/styles.css'
		])
	.pipe(concat('app.min.css'))
	.pipe(csso())
	.pipe(gulp.dest('static/css'));
});

gulp.task('vendor-js', function(){
	return gulp.src([
		'node_modules/jquery/dist/jquery.min.js',
		'node_modules/bootstrap/dist/js/bootstrap.min.js'
		])
	.pipe(concat('vendor.min.js'))
	.pipe(uglify())
	.pipe(gulp.dest('static/js'));
});

gulp.task('app-js', function(){
	return gulp.src([
		'node_modules/adminlte/dist/js/adminlte.min.js',
		'node_modules/initial-js/dist/initial.min.js',
		'assets/js/scripts.js'
		])
	.pipe(concat('app.min.js'))
	.pipe(uglify())
	.pipe(gulp.dest('static/js'));
});

gulp.task('fonts', function(){
	return gulp.src([
		'node_modules/bootstrap/fonts/*', 
		'node_modules/font-awesome/fonts/*',
		'node_modules/ionicons/dist/fonts/*'
		])
	.pipe(gulp.dest('static/fonts'));
});


//----//
gulp.task('default', [
	'clean', 
	'less', 
	'vendor-css', 
	'app-css',
	'vendor-js', 
	'app-js', 
	'fonts'
]);