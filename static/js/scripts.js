function openForm() {
    document.getElementById("myForm").style.display = "flex"
    document.getElementById("myWrapper").style.filter = "blur(4px)"
}

function closeForm() {
    document.getElementById("myForm").style.display = "none"
    document.getElementById("myWrapper").style.filter = "none"
}

document.addEventListener('DOMContentLoaded', function() {
    var icons = document.querySelectorAll('.clickable-icon');
    icons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            var taskId = this.getAttribute('data-task-id');
            var taskItem = this.closest('.all-tasks-list-item');

            fetch('/completed/' + taskId, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Apply fade-out animation
                        taskItem.classList.add('fade-out-animation');

                        // Toggle the line-through class based on the updated task status
                        if (data.completed) {
                            taskItem.classList.add('completed-task');
                        } else {
                            taskItem.classList.remove('completed-task');
                        }

                        // Refresh the list after a slight delay
                        setTimeout(() => {
                            window.location.reload(); // Reload the page to update the list
                        }, 500); // Adjust timing as needed
                    } else {
                        console.error('Task could not be updated.');
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
