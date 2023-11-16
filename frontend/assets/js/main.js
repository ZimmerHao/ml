
$("#pod-log-submit").click(function () {
    var podName = document.querySelector('#pod-name-input').value;
    $.ajax({
        type: 'GET',
        url: '/api/v1/kops/pod_log/',
        data: {"pod_name": podName},
        success: function (data) {
            $("#pod-log").val(data["lines"]);
        },
        dataType: "json"
    });
});

$("#yaml-url-submit").click(function () {
    var yamlURL = document.querySelector('#yaml-url-input').value;
    $.ajax({
        type: 'POST',
        url: '/api/v1/kops/apply_yaml/',
        contentType : 'application/json',
        data: JSON.stringify({"yaml_url": yamlURL}),
        success: function (data) {
            alert("create success");
        },
        dataType: "json"
    });
});

$("#yaml-url-delete").click(function () {
    var yamlURL = document.querySelector('#yaml-url-input').value;
    $.ajax({
        type: 'POST',
        url: '/api/v1/kops/delete_by_yaml/',
        contentType : 'application/json',
        data: JSON.stringify({"yaml_url": yamlURL}),
        success: function (data) {
            alert("delete success");
        },
        dataType: "json"
    });
});

$(".content-dashboard-pod button").click(function () {
    var podName = $(this).data("pod-name");
    // var logSocket = new WebSocket(
    //     'ws://' + window.location.host + '/ws/pod_log/' + podName + '/');
    //
    // logSocket.onmessage = function(e) {
    //     var data = JSON.parse(e.data);
    //     var message = data['message'];
    //     if (message != "") {
    //         document.querySelector('#pod-log').value += message;
    //     }
    // };
    //
    // logSocket.onclose = function(e) {
    //     console.error('Chat socket closed unexpectedly');
    // };
    //
    // logSocket.onopen = function(e) {
    //     logSocket.send(JSON.stringify({
    //         'message': "this is a request"
    //     }));
    // };

    $.ajax({
        type: 'GET',
        url: '/api/v1/kops/pod_log/',
        data: {"pod_name": podName},
        success: function (data) {
            $("#pod-log").val(data["lines"]);
        },
        dataType: "json"
    });
})
