function disappear() {
  $("#disappear_ul").toggleClass("hidden");
}

$(document).ready(function() {
  $("#popdown").click(disappear);
  $("#about").click();
  $("#home").click();
  $("#recipes").click();
  $("#map").click();
  $("#fridge").click();
  hidetext();
  }
)
