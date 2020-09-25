// https://stackoverflow.com/questions/59566549/how-to-do-delete-confirmation-for-a-table-data-with-bootstrap-modal-in-django

$(function () {
    $('#confirm-modal').on('show.bs.modal', function (event) {
        var message = $(event.relatedTarget).data('message');
        if (message) {
            $("#modal-message").html(message);
        }

        var url = $(event.relatedTarget).data('url');
        if (url) {
            $("#button-confirm-delete").click(function () {
                $('#form-confirm-modal').attr('action', url);
                $('#form-confirm-modal').submit();
            });
        }
    });
});


// document.addEventListener('DOMContentLoaded', () => {
//     let buttons = document.querySelectorAll("[data-target='#confirm-modal']");
//     if (buttons.length != 0) {
//         let form_confirm = document.querySelector('#form-confirm-modal')

//         buttons.forEach(button => {
//             button.addEventListener("click", () => {
    
//                 // extract texts from calling element and replace the modals texts with it
//                 if (button.dataset.message) {
//                     document.getElementById("modal-message").innerHTML = button.dataset.message;
//                 }
//                 // extract url from calling element and replace the modals texts with it
//                 if (button.dataset.url) {
//                     form_confirm.action = button.dataset.url;
//                 }
    
//             })
//         });
//         let button_confirm = document.getElementById("button-confirm-delete")
//         button_confirm.addEventListener('click', () => {
//             form_confirm.submit();
//         });
//     }

// });