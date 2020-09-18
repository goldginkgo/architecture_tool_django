$(document).ready(function () {
    /* home page */
    $.ajax({
        url: "/node_counts/",
        success: function (data) {
            console.log(data)
            $("#nodeloading").remove();
            $("#total_nodes").html(data);
        }
    });
    $.ajax({
        url: "/node_counts/",
        success: function (data) {
            $("#listloading").remove();
            $("#total_lists").html(data);
        }
    });
    $.ajax({
        url: "/node_counts/",
        success: function (data) {
            $("#graphloading").remove();
            $("#total_graphs").html(data);
        }
    });
    $.ajax({
        url: "/node_counts/",
        success: function (data) {
            $("#errorloading").remove();
            $("#total_errors").html(data);
        }
    });
});
