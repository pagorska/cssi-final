function disappearAdd() {
  $("#input").toggleClass("hidden");
}
function disappearItem(e) {
  $(e.target).toggleClass("hidden");
  id = e.target.innerHTML
  console.log(id)
  $(location).attr("href", "/?remove=" + id)
}
$(document).ready(function() {
  $("#add").click(disappearAdd);
  $(".item_info").click(disappearItem);
  }
)
