function disappearAdd() {
  $("#input").toggleClass("hidden");
}
function disappearItem() {
  $("#item_info").toggleClass("hidden");
}

$(document).ready(function() {
  $("#add").click(disappearAdd);
  $("#items").click(disappearItem);
  }
)
