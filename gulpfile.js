const gulp = require('gulp');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename');
const concat = require('gulp-concat');
const csso = require('gulp-csso');
const del = require('del');

gulp.task('clean', function(){
	del('static/*');
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

gulp.task('css', function(){
	return gulp.src([
		'node_modules/bootstrap/dist/css/bootstrap.min.css', 
		'node_modules/adminlte/dist/css/AdminLTE.css'
		])
	.pipe(concat('all.min.css'))
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


//----//
gulp.task('default', [
	'clean', 
	'vendor-css', 
	'js', 
	'css'
]);