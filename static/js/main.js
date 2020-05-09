function loginOrRegister(e) {
    let elementId = $(e).attr('value');
    $('#login').css('display', 'none');
    $('#register').css('display', 'none');
    $('#' + elementId + '').css('display', 'block')
}

function register(e) {
    let url = $(e).attr('post_to');
    if ($("#pw1").val().length >= 5 && validate() === 1) {
        let username = $('#username').val();
        let password = $('#pw1').val();
        $.post(url, {
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
                'username': username,
                'password': password,
            },
            function (callback) {
                is_success = callback['status'];
                if (is_success === '1') {
                    alert('注册成功，请登录');
                    $('#register').css('display', 'none');
                    $('#login').css('display', 'block');
                    $("input[name='username']").val(username);
                    $("input[name='password']").val(password);
                }
            }
        )
    }
}

function login(e) {
    let url = $(e).attr('post_to');
    let username = $("input[name='username']").val();
    let password = $("input[name='password']").val();
    let next = $(e).attr('next');
    if (password.length >= 5 && username !== "") {
        $.post(url, {
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
                'username': username,
                'password': password,
            },
            function (callback) {
                is_success = callback['status'];
                if (is_success === '0') {
                    $(e).parent().prev().prev().prev().css('display', 'block');
                } else {
                    location.href = next;
                }
            }
        )
    }
}

function closePanel(e) {
    $(e).parent().parent().parent().parent().parent().css('display', 'none')
}

function validate() {
    let is_true = 0;
    let pw1 = $("#pw1");
    let pw2 = $("#pw2");

    if (pw1.val() !== pw2.val()) {
        pw2.next().css('display', 'block');
        pw2.parent().addClass('has-error');
    } else {
        is_true = 1;
        pw2.next().css('display', 'none');
        pw2.parent().removeClass('has-error');
    }
    return is_true
}


function checkUsername(e) {
    let thisUsername = $(e).val()
}

function checkPassword(e) {
    let thisPassword = $(e).val()
}

function sendProfile(e) {
    let name = $(e).attr('name');
    let value = $(":input[name=" + name + "]").val();
    if (name === "gender") {
        value = $("input[name='gender']:checked").val();
        switch (value) {
            case '0':
                value = "保密";
                break;
            case '1':
                value = "男";
                break;
            case '2':
                value = "女";
                break;
        }
    }
    let url = $('#modify_user').attr('post_to')
    $.post(url, {
        'name': name,
        'value': value,
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
    }, function (event) {
    })
    $(e).parent().attr('value', '').css('display', 'none');
    $(e).parent().prev().css('display', 'block');
    $(e).parent().prev().children('span:first-child').children('span:last-child').text(value);
    if (name === "nickname") {
        $("h2[class='profile__heading--name']").children('span:first-child').text(value)
    }
}

function editSignature(e) {
    let signatureDiv = $(e).parent().parent().next().children('div:first-child');
    signatureDiv.css('display', 'none');
    let signature = signatureDiv.children('p:first-child').text();
    $(e).parent().parent().next().children('div:last-child').css('display', 'block').find('textarea').text(signature);
}

function sendSignature(e) {
    let signatureEditor = $(e).parent().parent().parent();
    let signature = signatureEditor.find('textarea').val();
    let url = $('#modify_user').attr('post_to')
    $.post(url, {
        'name': 'signature',
        'value': signature,
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
    }, function (event) {
    })
    signatureEditor.css('display', 'none');
    signatureEditor.prev().css('display', 'block').children('p:first-child').text(signature);
}

function editSignatureCancel(e) {

}

function startComment(e) {
    let commentForm = $(e).parent().parent().parent().next();
    if (commentForm.css('display') === 'block') {
        commentForm.css('display', 'none');
    } else {
        commentForm.css('display', 'block');
    }
}

function cancelComment(e) {
    $(e).parent().parent().css('display', 'none');
}

function like(e) {
    let article_id = $(e).val();
    let url = $(e).attr('comment_url');
    $.post(url,
        {'article_id': article_id, 'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()},
        function (callback) {
            console.log(callback)
        });
    if ($(e).text() === '已赞') {
        $(e).css('background-color', '#337ab7');
        $(e).text('点赞');
    } else {
        $(e).css('background-color', 'red');
        $(e).text('已赞');
    }
}

function articleSubmit(e) {
    if ($(e).attr('name') === 'published') {
        $("form[class='article-form']").append('<input name="status" value="published">').submit();
        alert('发布')
    } else {
        $("form[class='article-form']").append('<input name="status" value="draft">').submit();
        alert('保存')
    }
}

function sendMessage(e) {
    mes = $('#messageMessage').val()
    url = $(e).attr('post_to')
    conv_id = $(e).attr('conv_id')
    $.post(url,
        {
            'conv_id': conv_id,
            'message_detail': mes,
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        },
        function (callback) {
            console.log(callback)
        })
}

function sendComment(e) {
    alert($(e).prev().val());
}