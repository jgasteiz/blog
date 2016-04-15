'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    server = require('gulp-server-livereload');

gulp.task('webserver', function() {
    gulp.src('public')
        .pipe(server({
            livereload: true,
            directoryListing: false,
            open: true
        }));
});

gulp.task('sass', function () {
  return gulp.src('./static/scss/**/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(gulp.dest('./public/css'));
});

gulp.task('sass:watch', function () {
  gulp.watch('./static/scss/**/*', ['sass']);
});

gulp.task('default', ['sass', 'sass:watch', 'webserver']);
