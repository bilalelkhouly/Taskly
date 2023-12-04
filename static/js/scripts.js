function openTaskForm() {
    document.getElementById("myTaskForm").style.display = "flex"
    document.getElementById("myWrapper").style.filter = "blur(4px)"
}

function closeTaskForm() {
    document.getElementById("myTaskForm").style.display = "none"
    document.getElementById("myWrapper").style.filter = "none"
}

function openListForm() {
    document.getElementById("myListForm").style.display = "flex"
    document.getElementById("myWrapper").style.filter = "blur(4px)"
}

function closeListForm() {
    document.getElementById("myListForm").style.display = "none"
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

document.addEventListener('DOMContentLoaded', function() {
    var deleteIcons = document.querySelectorAll('.delete-icon');
    deleteIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            var taskId = this.getAttribute('data-task-id');

            fetch('/delete/' + taskId, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Reload the page to reflect the deletion
                        window.location.reload();
                    } else {
                        console.error('Task could not be deleted.');
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("your-lists-toggle");
    const dropdown = document.querySelector(".your-lists-dropdown");
    const arrowIcon = document.querySelector(".arrow-icon");

    toggleBtn.addEventListener("click", function(event) {
        event.preventDefault();
        
        console.log("Click event occurred"); 

        // Toggle the display property
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
            arrowIcon.classList.remove("rotated");
        } else {
            // Fetch list data using AJAX
            fetch('/get_lists')
                .then(response => response.json())
                .then(data => {
                    // Populate the dropdown with the fetched data
                    const listOptions = data.map(list => {
                        return `<li class="dropdown-list-item"><a href="/list/${list.title}">${list.title}</a></li>`;
                    });
                    dropdown.innerHTML = `<ul class="dropdown-ul">${listOptions.join('')}</ul>`;
                    dropdown.style.display = "block";
                    arrowIcon.classList.add("rotated");
                    console.log("Dropdown opened");
                })
                .catch(error => console.error(error));
        }
    });
});