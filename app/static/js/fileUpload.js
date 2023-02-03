function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function getStatus() {
    var status = 1;
    var status_bar = document.getElementById('id_progress');
    const i = setInterval(function (){
        if (status === 100) {
            clearInterval(i);
        }

        $.ajax({
            url: '/converter/uploads/status/',
            type: "GET",
            dataType: 'json',
            xhrFields: {
                withCredentials: true
            },
            success: function (result) {
                console.log(result.status);
                status = result.status;
                status_bar.ariaValueNow = status;
                status_bar.style.width = status + '%';
            }
        });
    }, 500)
}

(function(){
    var form = document.getElementById('file-form');
    var fileSelect = document.getElementById('id_file');
    var uploadButton = document.getElementById('submit');
    var extSelect = document.getElementById('id_select');
    var statusDiv = document.getElementById('status');

    form.onsubmit = function(event) {
        event.preventDefault();

        statusDiv.innerHTML = 'Uploading . . . ';

        // Get the files from the input
        var files = fileSelect.files;

        // Create a FormData object.
        var formData = new FormData();

        //Grab only one file since this script disallows multiple file uploads.
        var file = files[0];

        //Check the file type.
        if (!file.type.match('video.*')) {
            statusDiv.innerHTML = 'You cannot upload this file because it’s not an image.';
            return;
        }

        if (file.size >= 20000000000 ) {
            statusDiv.innerHTML = 'You cannot upload this file because its size exceeds the maximum limit of 2 MB.';
            return;
        }

         // Add the file to the AJAX request.
        formData.append('video', file, file.name);
        formData.append('output_format', extSelect.value);

        // Set up the request.
        var xhr = new XMLHttpRequest();

        // Open the connection.
        xhr.open('POST', '/converter/uploads/form/', true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken)


        // Set up a handler for when the task for the request is complete.
        xhr.onload = function () {
          if (xhr.status === 200) {
            statusDiv.innerHTML = 'Your upload is successful..';
            getStatus();
          } else {
            statusDiv.innerHTML = 'An error occurred during the upload. Try again.';
          }
        };

        // Send the data.
        xhr.send(formData);
    }
})();
