$(document).ready(function () {
    /* home page */
    $.ajax({
        url: "/node_counts/",
        success: function (data) {
            $("#nodeloading").remove();
            $("#total_nodes").html(data);
        }
    });
    $.ajax({
        url: "/listcount/",
        success: function (data) {
            $("#listloading").remove();
            $("#total_lists").html(data);
        }
    });
    $.ajax({
        url: "/graphcount/",
        success: function (data) {
            $("#graphloading").remove();
            $("#total_graphs").html(data);
        }
    });
    $.ajax({
        url: "/modeling/ajax/schema_count/",
        success: function (data) {
            $("#errorloading").remove();
            $("#schemas").html(data);
        }
    });
});
