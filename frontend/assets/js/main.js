document.querySelector('#pod-name-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#pod-log-submit').click();
        }
};

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
        data: {"yaml_url": yamlURL},
        success: function (data) {
            alert("create success");
        },
        dataType: "json"
    });
});