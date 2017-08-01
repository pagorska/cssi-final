function disappear() {
  $("#input").toggleClass("hidden");
}

$(document).ready(function() {
  $("#popdown").click();
  $("#about").click();
  $("#home").click();
  $("#recipes").click();
  $("#map").click();
  $("#fridge").click();
  $("#add").click(disappear);
  }
)
