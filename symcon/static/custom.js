$(document).ready(function() {
    $(document).on('submit', 'form.library-submit', function(e) {
        var form = $(this);
        if (form.data('submitted') == 'yes') {
            e.preventDefault();
        } else {
            form.data('submitted', 'yes');
        }

        return this;
    });
});
