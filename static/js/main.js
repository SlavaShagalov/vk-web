const server_address = 'http://127.0.0.1:8000';

function vote(object_id, object_type, vote_value) {
    const request = new Request(
        server_address + '/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            body: 'object_id=' + object_id + '&object_type=' + object_type + '&vote_value=' + vote_value
        }
    );

    fetch(request).then(
        function (response_raw) {
            response_raw.json().then(
                function (response_json) {
                    if (response_json.status === 'ok') {
                        console.log('OK: rating = ', response_json.rating);
                        if (object_type === 0) {
                            $("#question-rating-" + object_id).text(response_json.rating);
                        } else if (object_type === 1) {
                            $("#answer-rating-" + object_id).text(response_json.rating);
                        }
                    } else {
                        console.log('ERROR');
                    }
                }
            )
        }
    );
}

$(".question-vote-up").on('click', function (ev) {
    vote($(this).data('id'), 0, 1);
})

$(".question-vote-down").on('click', function (ev) {
    vote($(this).data('id'), 0, -1);
})

$(".answer-vote-up").on('click', function (ev) {
    vote($(this).data('id'), 1, 1);
})

$(".answer-vote-down").on('click', function (ev) {
    vote($(this).data('id'), 1, -1);
})

// correct answer handle
$('.form-check-input').click(function (ev) {
    console.log('.form-check-input clicked');

    let question_id = $(this).data('qid');
    let answer_id = $(this).data('aid');
    console.log('correct: ' + question_id + ' ' + answer_id);
    const request = new Request(
        server_address + '/correct/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            body: 'question_id=' + question_id + '&answer_id=' + answer_id
        }
    );

    fetch(request).then(
        function (response_raw) {
            response_raw.json().then(
                function (response_json) {
                    console.log('Got json: ', response_json);
                    if (response_json.status === 'ok') {
                        console.log('OK');
                        // убираем галочки со всех ответов на странице на случай, если предыдущий правильный
                        // ответ находится на данной странице (правильный ответ только один)
                        $('input[id^=answer-correct-]').each(function (i, el) {
                            $(this).prop("checked", false);
                        });

                        // меняем галочку у нового ответа
                        let checkbox = $("#answer-correct-" + answer_id);
                        checkbox.prop('checked', response_json.new_state);
                    } else {
                        console.log('ERROR');
                    }
                }
            )
        }
    );
})
