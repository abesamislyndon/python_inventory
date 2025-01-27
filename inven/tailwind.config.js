module.exports = {
    content: [
        // Templates in project templates directory
        '../../templates/**/*.html',
        // Templates in app directories
        '../../**/templates/**/*.html',
        // Python files containing Tailwind classes
        '../../**/forms.py'
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    500: '#6366f1', // Example color - use your desired color
                    600: '#4f46e5',
                    700: '#4338ca',
                    800: '#3730a3',
                }
            }
        },
    },
    plugins: [],
}