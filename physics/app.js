$(function() {
   $('a#show_hide').click(function(event){
     event.preventDefault();
     $('div#hide').toggle();
   });
 });
