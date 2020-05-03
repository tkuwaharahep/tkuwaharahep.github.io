$(function () {
  $("#toggle").click(function () {
    $("#menulist").slideToggle();
    return false;
  });
  $(window).resize(function () {
    var win = $(window).width();
    var p = 480;
    if (win > p) {
      $("#menulist").show();
    }
  });
});
