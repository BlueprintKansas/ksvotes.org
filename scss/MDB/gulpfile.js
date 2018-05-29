const gulp = require('gulp');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const cssmin = require('gulp-cssmin');
const browserSync = require('browser-sync').create();
const plugins = require('./js/modules');
const concat = require('gulp-concat');
const minify = require('gulp-minify');
const rename = require('gulp-rename');
const imagemin = require('gulp-imagemin');

// CSS Tasks
gulp.task('css-compile', function() {
  gulp.src('scss/**/*.scss')
    .pipe(sass({outputStyle: 'nested'}).on('error', sass.logError))
    .pipe(autoprefixer({
      browsers: ['last 10 versions'],
      cascade: false
    }))
    .pipe(gulp.dest('./dist/css/'));
});

gulp.task('css-minify', function() {
    gulp.src(['./dist/css/*.css', '!dist/css/*.min.css'])
      .pipe(cssmin())
      .pipe(rename({suffix: '.min'}))
      .pipe(gulp.dest('./dist/css'))
});

// JavaScript Tasks
gulp.task('js-build', function() {
  gulp.src(plugins.modules)
    .pipe(concat('mdb.js'))
    .pipe(gulp.dest('./dist/js/'))
});

gulp.task('js-minify', function() {
  gulp.src('./dist/js/mdb.js')
    .pipe(minify({
      ext:{
        // src:'.js',
        min:'.min.js'
      },
      noSource: true,
    }))
    .pipe(gulp.dest('./dist/js'));
});

// Image Compression
gulp.task('img-compression', function() {
  gulp.src('./img/*')
    .pipe(imagemin([
      imagemin.gifsicle({interlaced: true}),
      imagemin.jpegtran({progressive: true}),
      imagemin.optipng({optimizationLevel: 5}),
      imagemin.svgo({
        plugins: [
          {removeViewBox: true},
          {cleanupIDs: false}
        ]
      })
    ]))
    .pipe(gulp.dest('./dist/img'));
});

// Live Server
gulp.task('live-server', function() {
  browserSync.init({
    server: {
      baseDir: "./dist",
      directory: true
    },
    notify: false
  });

  gulp.watch("**/*", {cwd: './dist/'}, browserSync.reload);
});

// Watch on everything
gulp.task('mdb-go', function() {
  gulp.start('live-server');
  gulp.watch("scss/**/*.scss", ['css-compile']);
  gulp.watch(["dist/css/*.css", "!dist/css/*.min.css"], ['css-minify']);
  gulp.watch("js/**/*.js", ['js-build']);
  gulp.watch("dist/js/mdb.js", ['js-minify']);
  gulp.watch("**/*", {cwd: './img/'}, ['img-compression']);
});
