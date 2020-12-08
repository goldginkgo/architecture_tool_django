$(document).ready(function () {
    $("#exporting").hide();
    $('.export').on('click', function () {
        $("#exporting").show();
        $.ajax({
                url: '/export/',
            })
            .done((res) => {
                getStatus(res.task_id, res.export_filename);
            })
            .fail((err) => {
                console.log(err);
            });
    });

    function getStatus(taskID, filename) {
        $.ajax({
                url: `/tasks/${taskID}/`,
                method: 'GET'
            })
            .done((res) => {
                successCallback(res);
            })
            .fail((err) => {
                console.log(err)
            });

        function successCallback(res) {
            const taskStatus = res.task_status;
            if (taskStatus === 'SUCCESS') {
                $("#export-error").text("");
                $("#exporting").hide();
                window.location = `/download/${filename}.zip/`
                return false;
            }

            if (taskStatus === 'FAILURE') {
                $("#export-error").text("Export failed.");
                $("#exporting").hide();
                return false;
            }
            setTimeout(function () {
                getStatus(res.task_id, filename);
            }, 2000);
        }
    }

    Dropzone.autoDiscover = false;

    // Get the template HTML and remove it from the doumenthe template HTML and remove it from the doument
    var previewNode = document.querySelector("#template");
    previewNode.id = "";
    var previewTemplate = previewNode.parentNode.innerHTML;
    previewNode.parentNode.removeChild(previewNode);

    var myDropzone = new Dropzone(document.body, { // Make the whole body a dropzone
        url: "/import/", // Set the url
        maxFiles: 1,
        maxFilesize: 10,
        acceptedFiles: ".zip",
        headers: {
            "X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()
        },
        previewTemplate: previewTemplate,
        autoQueue: false, // Make sure the files aren't queued until manually added
        previewsContainer: "#previews", // Define the container to display the previews
        clickable: ".fileinput-button" // Define the element that should be used as click trigger to select files.
    });

    myDropzone.on("addedfile", function (file) {
        // Hookup the start button
        file.previewElement.querySelector(".start").onclick = function () {
            myDropzone.enqueueFile(file);
        };
    });

    // Update the total progress bar
    myDropzone.on("totaluploadprogress", function (progress) {
        document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
    });

    myDropzone.on("sending", function (file) {
        // Show the total progress bar when upload starts
        document.querySelector("#total-progress").style.opacity = "1";
        // And disable the start button
        file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
    });

    // Hide the total progress bar when nothing's uploading anymore
    myDropzone.on("queuecomplete", function (progress) {
        document.querySelector("#total-progress").style.opacity = "0";
    });

    // Setup the buttons for all transfers
    // The "add files" button doesn't need to be setup because the config
    // `clickable` has already been specified.
    document.querySelector("#actions .start").onclick = function () {
        myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
    };
    document.querySelector("#actions .cancel").onclick = function () {
        myDropzone.removeAllFiles(true);
    };
});
