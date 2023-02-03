function getStatus(task_id) {
    var status = 1;
    var status_bar = document.getElementById('id_progress');
    const i = setInterval(function (){
        if (status === 100) {
            clearInterval(i);
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
            }
        });
    }, 500)
}