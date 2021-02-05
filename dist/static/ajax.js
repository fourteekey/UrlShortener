$('#my_form').submit(function(e){
    e.preventDefault();
    $.ajax({
        url: "http://127.0.0.1:8000/api/v1/generator",
        type: "POST",
        dataType: "json",
        data: $('#my_form').serialize(),
        success: function(response) {
            let origin_url = $("#origin_url")[0].value;
            let short_url = response['short_url']
            let counter = 0;

            var my_table = $('#my_table');
            my_table.append(`<tr><td><a href="${origin_url}">${origin_url}</a></td><td><a href="/${short_url}">/${short_url}</a></td><td>${counter}</td></tr>`);

            $('#origin_url').val("");
            $('#short_url').val("");
            return false;
        },
        error: function(response) {
            let error_msg = response.responseJSON['detail_ru'];
            if (error_msg === undefined) {
                error_msg = response.responseJSON['detail']
            }
            alert(`Произошла ошибка. ${error_msg}`)
        }
    });
});