module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({

        // Lint our written JavaScript
        jshint : {
            main : ['static/dogecast/js/*.js'],
            'options' : {
                'jshintrc' : true,
            }
        },

        // Concatenate & minify JS files
        uglify: {
            api: {
                files: {
                    'static/dogecast/js/build/dogecast.1.0.0.min.js': [
                        'static/dogecast/js/main.js',
                    ]
                }
            },
        },

        // Concatenate & minify CSS files
        cssmin: {
            target: {
                files: {
                    'static/dogecast/css/combined.1.0.0.min.css': [
                        'static/dogecast/css/vendor/reset.css',
                        'static/dogecast/css/styles.css'
                    ],
                }
            },

            options : {
                keepSpecialComments : 0
            }
        },

        // Shell commands
        shell: {

            serve : {
                command: './main.py',
                options: {
                    execOptions: {
                        maxBuffer: 0x100000000,
                    }
                }
            },

        },

    });

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-shell');

    /* Run:
     *
     *
     */
    grunt.registerTask('default', ['uglify', 'cssmin']);
    grunt.registerTask('serve', ['shell:serve']);

};
