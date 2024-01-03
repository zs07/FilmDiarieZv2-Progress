$(document).ready(function () {
    // Initialize Select2 for movie name input
    $('input[name="movie_name"]').select2({
        placeholder: 'Movie Name',
        allowClear: true,
        ajax: {
            url: 'https://api.themoviedb.org/3/search/movie',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    query: params.term,
                    api_key: '1e7d2dc4614da27675b4b0ebeedb646a',
                };
            },
            processResults: function (data) {
                return {
                    results: $.map(data.results, function (movie) {
                        return {
                            id: movie.id,
                            text: movie.title + ' (' + (movie.release_date ? movie.release_date.split('-')[0] : 'N/A') + ')',
                            details: 'https://www.themoviedb.org/movie/' + movie.id,
                        };
                    }),
                };
            },
            cache: true,
        },
        minimumInputLength: 1,
    });

    // Handle movie name selection
    $('input[name="movie_name"]').on('select2:select', function (e) {
        var data = e.params.data;
        console.log(data.text);
        $(this).val(data.text);

        var form = $(this).closest('form');
        form.find('#details').val(data.details);

        // Fetch movie images using the movie ID
        $.ajax({
            url: 'https://api.themoviedb.org/3/movie/' + data.id + '/images',
            dataType: 'json',
            data: {
                api_key: '1e7d2dc4614da27675b4b0ebeedb646a',
            },
            success: function (response) {
                var posters = response.posters.slice(0, 20);

                // Initialize Select2 for poster dropdown
                var posterDropdown = form.find('input[name="poster"]');
                posterDropdown.select2({
                    templateResult: formatPoster,
                    templateSelection: formatPosterSelection,
                    data: $.map(posters, function (poster, index) {
                        return {
                            id: index,
                            imageUrl: 'https://image.tmdb.org/t/p/w500' + poster.file_path,
                            url: 'https://image.tmdb.org/t/p/w500' + poster.file_path,
                        };
                    }),
                });

                posterDropdown.trigger('change');
            },
            error: function () {
                // Display a message if there is an issue connecting to TMDB
                alert('Error connecting to TMDB. Please try again later.');
            },
        });
    });

    // Format the poster in the dropdown
    function formatPoster(poster) {
        if (!poster.id) {
            return poster.text;
        }

        var $poster = $(
            '<div class="poster-result">' +
            '<img class="poster-image" src="' + poster.imageUrl + '" /> ' +
            '</div>'
        );
        return $poster;
    }

    // Format the poster selection
    function formatPosterSelection(poster) {
        return "Poster Selected";
    }

    // Handle poster selection
    $('input[name="poster"]').on('select2:select', function (e) {
        var data = e.params.data;

        var posterContainer = $('#poster-container');
        var selectedPoster = $('#selected-poster');

        selectedPoster.attr('src', data.imageUrl);
        selectedPoster.css('display', 'block');
        posterContainer.css('display', 'block');

        $('input[name="poster"]').val(data.url);
    });
});
