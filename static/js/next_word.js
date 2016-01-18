$(document).ready(function() {

  $( ".predict" ).on( "click", function() {
    console.log( $('.text').val() );
    $('.word').remove();

          $.ajax({
            method: "POST",
            url: "./next_word",
            data: { text: $('.text').val()},
            dataType: "json",
        }).done(function(words){
            for (var i in words){
                $(".words").append('<p class="word" >' + words[i] + '</p>');
            }
        });


  });

} );

