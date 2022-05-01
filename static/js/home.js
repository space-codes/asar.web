// Download the entry
function setDownload(pred_id){
  var send = pred_id.toString();
  $.ajax({
    type: "POST",
    url: "/download_result/",
    data: send,
    success: function(data){
        console.log(data);
        var filename = "result.txt"
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + data);
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
  });
}
// Delete the prediction
function deleteEntry(pred_id){
  var send = pred_id.toString();
  Swal.fire({
  title: 'Are you sure?',
  text: "You won't be able to revert this!",
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, delete it!'
}).then((result) => {
  if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: "/delete_result/",
        data: send,
        success: function(data){
          location.reload();
        }
      });
  }
})
}
