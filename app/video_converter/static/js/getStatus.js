
function download(task_id) {
    var button = document.getElementById("id_download");
    button.href = "/converter/download/" + task_id + "/";
    button.style.display = "";
}


function getStatus(task_id) {
    var status = 1;
    var status_bar = document.getElementById('id_progress');
    const i = setInterval(function (){
        if (status === 100) {
            clearInterval(i);
            download(task_id)
        }

        $.ajax({
            url: '/converter/uploads/status/' + task_id +'/',
            type: "GET",
            dataType: 'json',
            xhrFields: {
                withCredentials: true
            },
            success: function (result) {
                console.log(result.progress);
                status = result.progress;
                status_bar.ariaValueNow = status;
                status_bar.style.width = status + '%';
            },
            error: function () {
                clearInterval(i);
                alert("error")

            }
        });
    }, 500)
}