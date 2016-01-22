$(document).ready(function() {

    $('#noresults').hide();
    $('#results').hide();
    $('#instructions').show();

  $( '#forceprediction' ).on( 'click', function() {
    $('.bigram').remove();
    $('.trigram').remove();
    $('.fourgram').remove();

      $.ajax({
        method: 'POST',
        url: './predict',
        data: { text: $('.text').val()},
        dataType: 'json',
        }).done(function(tokens){
            console.log(tokens.length);
            if ($('.text').val().length == 0){
                $('#noresults').hide();
                $('#results').hide();
                $('#instructions').show();
            }
            else if (tokens.length == 0) {
                $('#noresults').show();
                $('#results').hide();
                $('#instructions').hide();
            }

            else {
                $('#noresults').hide();
                $('#results').show();
                $('#instructions').hide();
            }
            for (var i in tokens){
                if (tokens[i].ngram == '4'){
                    $('.fourgrams').append('<button type="button" class="fourgram btn btn-success">' + tokens[i].l4.trim() + '</button>');
                }
                if (tokens[i].ngram == '3'){
                    $('.trigrams').append('<button type="button" class="trigram btn btn-info">' + tokens[i].l4.trim() +  '</button>');
                }
                if (tokens[i].ngram == '2'){
                    $('.bigrams').append('<button type="button" class="bigram btn btn-warning">' + tokens[i].l4.trim() +  '</button>');
                }
            }
        });
  });

    $('body').on('keydown', '#message', function(k){
        if (k.which == 32) {
            $('#forceprediction').trigger('click');
        }
    });

    $('table').on( 'click', 'button', function() {
        $('.text').val($('.text').val() + $(this).html() + ' ');
        $('.text').focus();
        $('#forceprediction').trigger('click');
    })

    $('#clearmsg').on( 'click', function() {
        $('.text').val('');
        $('.text').focus();
        $('#noresults').hide();
        $('#results').hide();
        $('#instructions').show();
    })

} );

