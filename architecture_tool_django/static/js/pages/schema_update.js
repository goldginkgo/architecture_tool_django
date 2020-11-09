$(function () {
    var te = document.getElementById("codemirror_modal");
    var editor_diff = CodeMirror.fromTextArea(te, {
        mode: "text/x-diff",
        theme: "monokai",
    });

    $('#modal-diff').on('shown.bs.modal', function (e) {
        $.ajax({
            url: "/api/schemas/" + $('input[name=key]').attr("value"),
            success: function (data) {
                original = JSON.stringify(data.schema, null, 2);
                ta_str = editor_json.getValue()
                updated = JSON.stringify(JSON.parse(ta_str), null, 2);
                editor_diff.setValue(Diff.createPatch("", original, updated))
            }
        });

    })
});
