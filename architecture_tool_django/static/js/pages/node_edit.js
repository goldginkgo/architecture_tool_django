var te = document.getElementById("codemirror_modal");
var editor_diff = CodeMirror.fromTextArea(te, {
    mode: "text/x-diff",
    theme: "monokai",
});

$('#modal-diff').on('shown.bs.modal', function (e) {
    $.ajax({
        url: "/api/nodes/" + $('#nodekey').data('node-key'),
        success: function (data) {
            original = JSON.stringify(data, null, 2);
            ta_str = editor_json.getValue()
            updated = JSON.stringify(JSON.parse(ta_str), null, 2);
            editor_diff.setValue(Diff.createPatch("", original, updated))
        }
    });
})
