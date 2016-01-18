$(document).ready(function() {

  $( ".predict" ).on( "click", function() {
    console.log( $( this ).text() );
    $('.word').remove();

          $.ajax({
            method: "POST",
            url: "./predict",
            data: { text: $('.text').val()},
            dataType: "json",
        }).done(function(words){
            for (var i in words){
                $(".words").append('<option class="word" value="' + words[i].l4 + '">' + words[i].l4 + '</option>');
            }
        });


  });

} );

