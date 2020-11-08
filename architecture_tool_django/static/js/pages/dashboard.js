$(function () {
    /* home page */
    $.ajax({
        url: "/api/nodes/",
        success: function (data) {
            $("#nodeloading").remove();
            $("#total_nodes").html(data.length);
        }
    });
    $.ajax({
        url: "/api/lists/",
        success: function (data) {
            $("#listloading").remove();
            $("#total_lists").html(data.length);
        }
    });
    $.ajax({
        url: "/api/graphs/",
        success: function (data) {
            $("#graphloading").remove();
            $("#total_graphs").html(data.length);
        }
    });
    $.ajax({
        url: "/api/schemas/",
        success: function (data) {
            $("#errorloading").remove();
            $("#schemas").html(data.length);
        }
    });
});
