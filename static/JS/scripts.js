function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.dataset.taskId);
}

function drop(ev) {
    ev.preventDefault();
    var taskId = ev.dataTransfer.getData("text");
    var newCategory = ev.target.closest('.task-list').dataset.category;
    
    fetch(`/update_category/${taskId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `category=${encodeURIComponent(newCategory)}`
    }).then(() => {
        location.reload();
    });
}

// ... (keep the existing editTask, deleteTask, and getCookie functions)


function editTask(taskId) {
    const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
    const taskTitle = taskElement.firstChild.textContent.trim();
    const newTitle = prompt("Edit task:", taskTitle);
    
    if (newTitle !== null && newTitle !== "") {
        fetch(`/update/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `title=${encodeURIComponent(newTitle)}`
        }).then(() => {
            location.reload();
        });
    }
}

function deleteTask(taskId) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`/delete/${taskId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(() => {
            location.reload();
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}