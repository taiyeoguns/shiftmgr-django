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
		'assets/css/shiftmgr.css'
		])
	.pipe(concat('app.min.css'))
	//.pipe(gulp.dest('static/css'))
	//.pipe(rename('all.min.css'))
	.pipe(csso())
	.pipe(gulp.dest('static/css'));
});

gulp.task('js', function(){
	//console.log('working');
	return gulp.src('node_modules/adminlte/dist/js/adminlte.js')
	.pipe(rename('adminlte.min.js'))
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
	//'js', 
	'app-css',
	'fonts'
]);