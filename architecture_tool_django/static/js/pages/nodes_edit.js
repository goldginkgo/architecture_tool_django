$(function () {
    var nodekey = $('#nodekey').attr("data-nodekey");
    var nodetype = $('#nodetype').attr("data-nodetype-key");
    //function to initialize select2
    function initializeEdgetypeSelect() {
        $('select.edgetype-select').select2({
            theme: 'bootstrap4',
            placeholder: "Edge Type",
            ajax: {
                url: '/api/nodetypes/' + nodetype + '/edgetypes/',
                dataType: 'json',
                delay: 250
            }
        });
    }

    function initializeTargetNodeSelect() {
        $("select.node-select").select2({
            theme: 'bootstrap4',
            placeholder: "Target Node",
            ajax: {
                url: "/api/nodes/targetnodes/",
                dataType: 'json',
                data: function (params) {
                    var query = {
                        q: params.term,
                        edgetype_id: $(this).attr("data-edgetype-id")
                    }
                    return query;
                },
                delay: 250
            }
        });
    }
    // bs-stepper
    var stepper = new Stepper($('.bs-stepper')[0], {
        //animation: true
    });
    $('.step-previous').on('click', function () {
        stepper.previous();
    });
    $('.step-next').on('click', function () {
        stepper.next();
    });
    var stepperElem = document.getElementById('mystepper');
    var form = $(".bs-stepper-content form");
    stepperElem.addEventListener('show.bs-stepper', function (event) {
        form.removeClass('was-validated');
        if (event.detail.from == 0) {
            const errors = editor.validate();

            if (errors.length) {
                event.preventDefault();
                // console.log(errors);
            }
        }
        if (event.detail.from == 1 && event.detail.to == 2) {
            var empty_edges = $('.edgetype-select').filter(function () {
                return $(this).val() === null
            }).length

            var empty_nodes = $('.node-select').filter(function () {
                return $(this).val() === null
            }).length

            if (empty_edges || empty_nodes) {
                event.preventDefault();
                form.addClass('was-validated');
            }
        }
    })

    // json-editor
    JSONEditor.defaults.options.theme = 'bootstrap4';
    JSONEditor.defaults.options.iconlib = 'fontawesome5';
    $.ajax({
        url: "/api/nodetypes/" + nodetype,
        success: function (data) {
            schema_key = data.attribute_schema;

            $.ajax({
                url: "/api/schemas/" + schema_key + "/",
                success: function (data) {
                    //editor.destroy();
                    $('#editor_holder').empty();
                    editor = new JSONEditor(document.getElementById('editor_holder'), {
                        schema: data.schema,
                        disable_collapse: true,
                        disable_edit_json: true,
                        disable_properties: true,
                        display_required_only: false,
                        //show_opt_in: true,
                        show_errors: "always"
                    });
                    $('.je-object__title').remove();
                    $.ajax({
                        url: '/api/nodes/' + nodekey,
                        dataType: 'json',
                        contentType: 'application/json',
                        success: function (data, textStatus, jQxhr) {
                            editor.setValue(data.attributeSet)
                        }

                    })

                }
            });
        }
    });

    // Show attributeSet differences
    var te = document.getElementById("codemirror_modal");
    var editor_diff = CodeMirror.fromTextArea(te, {
        mode: "text/x-diff",
        theme: "monokai",
    });
    $('#modal-diff').on('shown.bs.modal', function (e) {
        $.ajax({
            url: "/api/nodes/" + nodekey,
            success: function (data) {
                original = JSON.stringify(data.attributeSet, null, 2);
                ta_str = editor.getValue();
                updated = JSON.stringify(ta_str, null, 2);
                editor_diff.setValue(Diff.createPatch("", original, updated))
            }
        });
    })

    // select for preselected edges
    initializeEdgetypeSelect()
    initializeTargetNodeSelect()

    // Fetch the preselected item, and add to the control
    $('.edge-row').each(function () {
        var edgetypeSelect = $(this).find('select.edgetype-select')
        var nodeSelect = $(this).find('select.node-select')

        $.ajax({
            type: 'GET',
            url: '/api/edgetypes/' + edgetypeSelect.attr("data-edge-type-id") + '/select/'
        }).then(function (data) {
            // create the option and append to Select2
            var option = new Option(data.text, data.id, true, true);
            edgetypeSelect.append(option).trigger('change');

            // manually trigger the `select2:select` event
            edgetypeSelect.trigger({
                type: 'select2:select',
                params: {
                    data: data
                }
            });
        });

        $.ajax({
            type: 'GET',
            url: '/api/nodes/' + nodeSelect.attr("data-target-node") + '/targetnode/'
        }).then(function (data) {
            // create the option and append to Select2
            var option = new Option(data.text, data.id, true, true);
            nodeSelect.append(option).trigger('change');

            // manually trigger the `select2:select` event
            nodeSelect.trigger({
                type: 'select2:select',
                params: {
                    data: data
                }
            });
        });

    });

    // edges
    $("#add-edge").on("click", function () {
        $("#edges").prepend(`<div class="row edge-row">
                            <div class="col-sm-5">
                              <div class="form-group">
                                <select class="form-control select edgetype-select" required></select>
                                <div class="invalid-feedback"><strong>This field is required.</strong></div>
                              </div>
                            </div>
                            <div class="col-sm-5">
                              <div class="form-group">
                                <select class="form-control select node-select" required></select>
                                <div class="invalid-feedback"><strong>This field is required.</strong></div>
                              </div>
                            </div>
                            <div class="col-sm-2">
                              <a class="btn remove-edge" style="color:red">
                                <i class="fas fa-trash remove-edge">
                                </i>
                              </a>
                            </div>
                          </div>`);

        initializeEdgetypeSelect()
        initializeTargetNodeSelect()

        $('select.edgetype-select').on('select2:select', function (e) {
            var data = e.params.data;
            // clear node-select selection
            $(this).closest('div.edge-row').find('select.node-select').val(null).trigger('change');
            // add data-edgetype-id to node-select
            $(this).closest('div.edge-row').find('select.node-select').attr("data-edgetype-id", data.id);
            // add data-edge-type to edgetype-select
            $(this).closest('div.edge-row').find('select.edgetype-select').attr("data-edge-type",
                data.edge_type);
        });

    });

    $(document).on("click", ".remove-edge", function () {
        $(this).closest('div.row').remove();
    });
});

// create node
$("#submit-data").click(function (e) {
    e.preventDefault();
    edges = []
    $('.edge-row').each(function () {
        var edge = {
            edge_type: $(this).find('select.edgetype-select').attr("data-edge-type"),
            target: $(this).find('select.node-select').val()
        }

        edges.push(edge);
    });
    var nodedata = {
        key: $('#nodekey').attr("data-nodekey"),
        nodetype: $('#nodetype').attr("data-nodetype-key"),
        attributeSet: editor.getValue(),
        outbound_edges: edges
    }
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()
        }
    });
    console.log($('#nodekey').attr("data-nodekey"));
    $.ajax({
        type: 'put',
        url: '/api/nodes/' + $('#nodekey').attr("data-nodekey") + '/',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(nodedata),
        success: function (data, textStatus, jQxhr) {
            window.location.href = "/nodes/" + $('#nodekey').attr("data-nodekey");
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(jqXhr)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })

})
