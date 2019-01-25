/**
 * 前端自动化管理工具gulp配置
 */
var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var livereload = require('gulp-livereload');
var shell = require('gulp-shell');
var cleanCss = require('gulp-clean-css');
var sourcemaps = require('gulp-sourcemaps');

var jsFiles = "app/static/scripts/*.js";
var prod_jsDict = "app/static/dist/scripts/";
var styleFile = "app/static/styles/scss/*.scss";
var prod_styleDict = "app/static/dist/styles/css/";
var styleDict = "app/static/styles/css/";
//指定按顺序运行一组任务 default任务由数组中的任务组成
gulp.task('default', ['start_server','watch', 'build_style', 'build_scripts'], function() {}

);

// 编译并压缩css
gulp.task('build_style', function(){
    return gulp.src(styleFile)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        // .pipe(gulp.dest(styleDict))
        .pipe(cleanCss({debug: true}, function(details) {
            console.log(details.name + ': ' + details.stats.originalSize);
            console.log(details.name + ': ' + details.stats.minifiedSize);
        }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(prod_styleDict))
        // .pipe(livereload()); 
});

// 压缩js源码
gulp.task('build_scripts', function(){
    return gulp.src(jsFiles)
        .pipe(uglify())
        .pipe(gulp.dest(prod_jsDict))
});

// 监视文件更改
gulp.task('watch', function(){
    livereload.listen();
    gulp.watch(styleFile, ['build_style']);
    gulp.watch(jsFiles, ['build_scripts']);
});

//执行python服务器启动脚本 先激活了虚拟环境
gulp.task('start_server',shell.task(['. venv/bin/activate && python runserver.py']));