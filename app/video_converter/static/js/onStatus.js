$( document ).ready(function(){
    var task_id = document.getElementById('task_id').value;
    console.log(task_id);
    if (task_id) {
        getStatus(task_id);
    }
});