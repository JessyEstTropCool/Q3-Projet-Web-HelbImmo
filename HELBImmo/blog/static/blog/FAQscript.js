
    //opens confirmation tab
    function js_open()
    {
        $(this).parent().siblings('.js-confirm').show();
        $(this).closest('.js-initial').hide();
        
    }

    //sets back to initial state
    function js_cancel()
    {
        $(this).parent().siblings('.js-initial').show();
        $(this).closest('.js-confirm').hide();
    }

    //request to delete a question
    function del_question()
    {
        let btn = $(this);
        $.ajax({
            url: btn.data('url'),
            success: function (result) 
            {
                btn.closest('.js-question').remove();
            }
        });
    }

    //request to delete an answer
    function del_reponse()
    {
        let btn = $(this);
        $.ajax({
            url: btn.data('url'),
            success: function (result) 
            {
                form = document.createElement('div');
                form.innerHTML = result;
                form = $(form);

                btn.closest('.js-reponse').empty().append(form);

                form.find('.js-open').click(js_open);
                form.find('.js-cancel').click(js_cancel);
                form.find('.js-answer').click(post_reponse);
            }
        });
    }

    //request to send an answer
    function post_reponse()
    {
        let btn = $(this)
        $.ajax({
            type: 'POST',
            url: btn.data('url'),
            data: {
                'content': btn.siblings('.js-answer-content').val(),
                csrfmiddlewaretoken: btn.siblings('input[name=csrfmiddlewaretoken]').val(),
                'questionid': btn.data('question')
            },
            success: function(data){
                reponse = document.createElement('div');
                reponse.innerHTML = data;
                reponse = $(reponse);

                reponse.find('.js-open').click(js_open);
                reponse.find('.js-cancel').click(js_cancel);
                reponse.find('.js-del-reponse').click(del_reponse);

                btn.closest('.js-reponse').empty().append(reponse);
            }
        });
    }

    //request to send a question
    $('#question_form').submit(function (e) {
        e.preventDefault();
        let info = $('#question_form_data');
        $.ajax({
            type: 'POST',
            url: info.data('url'),
            data: {
                'question': $('#question_form textarea').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                'postid': info.data('postid')
            },
            success: function(data){
                question = document.createElement('div');
                question.innerHTML = data;
                question = $(question);

                question.find('.js-open').click(js_open);
                question.find('.js-cancel').click(js_cancel);
                question.find('.js-del-question').click(del_question);
                question.find('.js-del-reponse').click(del_reponse);
                
                $('#question_form textarea').val('');
                $('#question_zone').prepend(question);    
                $('#noQuestions').remove();
            }
        });
    });

    //set the appropriate event handlers to corresponding classes
    $(document).ready(function () {
        $(".js-del-question").click(del_question);

        $(".js-del-reponse").click(del_reponse);

        $(".js-open").click(js_open);

        $(".js-cancel").click(js_cancel);

        $('.js-answer').click(post_reponse);
    });