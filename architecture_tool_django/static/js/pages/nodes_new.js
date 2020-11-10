$(function () {
    // json-editor
    JSONEditor.defaults.options.theme = 'bootstrap4';
    JSONEditor.defaults.options.iconlib = 'fontawesome5';


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
        if (event.detail.from == 0 && (!$("#nodekey").val().trim() || !$("#nodetype").val())) {
            event.preventDefault();
            form.addClass('was-validated');
        }
        if (event.detail.from == 1 && event.detail.to == 2) {
            const errors = editor.validate();

            if (errors.length) {
                event.preventDefault();
            }
        }
        if (event.detail.from == 2 && event.detail.to == 3) {
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


    // node type
    // TODO support pagination
    $('#nodetype').select2({
        theme: 'bootstrap4',
        placeholder: "Node Type",
        allowClear: true,
        ajax: {
            url: '/api/nodetypes/select2/',
            dataType: 'json',
            delay: 250
        }
    });
    // change json editor and edges when node type changes
    $('#nodetype').on('change', function () {
        $.ajax({
            url: "/api/nodetypes/" + this.value,
            success: function (data) {
                schema_key = data.attribute_schema;
                $.ajax({
                    url: "/api/schemas/" + schema_key + "/",
                    success: function (data) {
                        //editor.destroy();
                        $('#edges').empty();
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
                    }
                });
            }
        });
    });


    // Edges
    // Add edges
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
                            </div>`
                            );

        $("#edges").find('select.edgetype-select').first().select2({
            theme: 'bootstrap4',
            placeholder: "Edge Type",
            ajax: {
                url: '/api/nodetypes/' + $('#nodetype').val() + '/edgetypes/',
                dataType: 'json',
                delay: 250
            }
        });

        $("#edges").find('select.edgetype-select').first().on('select2:select', function (e) {
            var data = e.params.data;
            // clear node-select selection
            $(this).closest('div.edge-row').find('select.node-select').val(null).trigger('change');
            // add data-edgetype-id to node-select
            $(this).closest('div.edge-row').find('select.node-select').attr("data-edgetype-id", data.id);
        });

        $("#edges").find('select.node-select').first().select2({
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
    });
    // Remove edges
    $(document).on("click", ".remove-edge", function () {
        $(this).closest('div.row').remove();
    });

    // Submit data
    $("#submit-data").click(function (e) {
        e.preventDefault();
        edges = []
        $('.edge-row').each(function () {
            var edge = {
                edge_type: $(this).find('select.edgetype-select').select2('data')[0].edge_type,
                target: $(this).find('select.node-select').val()
            }

            edges.push(edge);
        });
        var nodedata = {
            key: $("input#nodekey").val(),
            nodetype: $("select#nodetype").val(),
            attributeSet: editor.getValue(),
            outbound_edges: edges
        }

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()
            }
        });
        $.ajax({
            type: 'post',
            url: '/api/nodes/',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(nodedata),
            success: function (data, textStatus, jQxhr) {
                window.location.href = "/nodes/" + $("input#nodekey").val() + "/";
            },
            error: function (jqXhr, textStatus, errorThrown) {
                $('#node-validate').text(jqXhr.responseText)
                // console.log(jqXhr.responseText)
                // console.log(textStatus)
                // console.log(errorThrown)
            }
        })

    })
})
