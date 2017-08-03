function disappearAdd() {
  $("#input").toggleClass("hidden");
}
function disappearItem(e) {
  $(e.target).toggleClass("hidden");
}

$(document).ready(function() {
  $("#add").click(disappearAdd);
  $(".item_info").click(disappearItem);
  }
)
