document.addEventListener("DOMContentLoaded", function () {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'))
    toastElList.map(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl)
        toast.show()
    });
    const deleteModal = document.getElementById('deleteModal');

    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget; // Button that triggered the modal
            const noteId = button.getAttribute('data-note-id'); // Extract note ID

            const form = document.getElementById('deleteForm');

            const noteTitle = button.getAttribute('data-note-title')

            // Update form action dynamically
            form.action = form.dataset.baseUrl.replace('0', noteId);

            const modalBody = deleteModal.querySelector('.modal-body p');

            modalBody.textContent = `Are you sure you want to delete '${noteTitle}', this action cannot be undone!`;
        });
    }

    const deleteModalCat = document.getElementById('deleteModalCategory');
    if (deleteModalCat) {
        deleteModalCat.addEventListener('show.bs.modal', (event) => {
            const button = event.relatedTarget;

            const noteId = button.getAttribute('data-note-id');

            const categoryId = button.getAttribute('data-category-id');

            const form = document.getElementById('deleteFormCategory');

            const noteTitle = button.getAttribute('data-note-title')

            form.action = form.dataset.baseUrl.replace('NOTE_ID', noteId).replace('CATEGORY_ID', categoryId)

            const modalBody = deleteModalCat.querySelector(".modal-body p");
            modalBody.textContent = `Are you sure you want to delete '${noteTitle}', this action cannot be undone!`;
        });
    }

    const favBtn = document.querySelectorAll(".fav-btn")
    favBtn.forEach(btn => {
        let icon = btn.querySelector('.favorite_icon')
        let fav = btn.getAttribute("note-is-fav")
        if (fav === 'False') {
            fillStar(btn, icon, 'mouseenter')
            emptyStar(btn, icon, "mouseleave")
        }
        else if (fav === 'True') {
            fillStar(btn, icon, 'mouseleave')
            emptyStar(btn, icon, "mouseenter")
        }

    })


    function fillStar(btn, icon, action) {
        btn.addEventListener(action, () => {
            icon.classList.remove("bi-star");
            icon.classList.add("bi-star-fill");
        });
    }
    function emptyStar(btn, icon, action) {
        btn.addEventListener(action, () => {
            icon.classList.remove("bi-star-fill");
            icon.classList.add("bi-star");
        })
    }
});
