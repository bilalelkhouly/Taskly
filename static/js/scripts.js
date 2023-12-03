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
            var path = this.querySelector('path');
            if (path.style.stroke === 'green') {
                path.style.stroke = 'white';
            } else {
                path.style.stroke = 'green';
            }
        });
    });
});
