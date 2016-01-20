var gulp = require('gulp');
var typescript = require('gulp-typescript');
var typescriptAngular = require('gulp-typescript-angular');


gulp.task('scripts', function () {
  return gulp.src('./media_src/SimpleERP.ts')
    .pipe(typescript())
    .pipe(typescriptAngular({
      decoratorModuleName:'SimpleERP'
    }))
    .pipe(gulp.dest('./media/simpleerp'));
});


gulp.task('default', function() {
    gulp.start('scripts');
  // place code for your default task here
});
