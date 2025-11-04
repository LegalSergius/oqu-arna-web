document.addEventListener('DOMContentLoaded', () => {
    const createCourseCard = document.getElementById('createCourseCard');
    
    createCourseCard.addEventListener('click', () => {
        fetch('/courses/create/')
            .then(response => response.json())
            .then(data => {
                const error = data.error;

                if (error) {
                    alert(error)
                } else {
                    const courseModalContainer = document.getElementById('courseModalWindow');
                    courseModalContainer.innerHTML = data.html;
                    const courseCreateModal = document.getElementById('courseCreateModal');

                    new bootstrap.Modal(courseCreateModal).show();

                    courseCreateModal.addEventListener('shown.bs.modal', function () {
                        console.log('modalEl - ', courseCreateModal);
                        const fileNameLabel = document.getElementById('fileNameLabel');
                        const input = document.getElementById('id_guideline_upload');
                        input.addEventListener('change', function () {
                            const file = input.files[0];
                            if (file) {
                                fileNameLabel.textContent = file.name;
                                console.log('file - ', file, file.name)
                            } 
                        });
                    });
                }
            });
    });    
});