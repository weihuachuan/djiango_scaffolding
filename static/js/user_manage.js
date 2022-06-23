// 获取表单数据逻辑代码

// 获取新增人員信息
$('#user_add > form').on('submit', function (e) {
    // 阻止默认提交事件
    e.preventDefault();
    // 采集用户信息
    var user_obj = get_add_user_data();
    $.ajax({
        type: "post",
        url: "/user/add_or_update_user/",
        data:{"flag": "add","data":JSON.stringify(user_obj)},
        dataType: "json",
        success: res => {
            if (res.status) {
               $('#add_message').text(res.msg);
               close_pop_div('user_add');
               clear_data('#add_');
               //刷新页面
               window.location.reload()
            }else{
                $('#add_message').text(res.msg);
            }
        },
        error: () => {
            console.log('没有连接到服务器')
        }
    });
})

// 获取人員修改信息
function edit(obj) {
        var user_id = $(obj).parent().parent().parent().find('.tb_user_id').text();
        $.ajax({
        type: "post",
        url: "/user/find_user_detail/",
        data:{'user_id': user_id},
        dataType: "json",
        success: res => {
            if (res.status) {
                $('#edit_user_name').val(res.data.user_name);
                $('#edit_user_id').val(res.data.user_id);
                $('#edit_phone_num').val(res.data.phone);
                $('#edit_authority').val(res.data.permission);
                $('#edit_user_password').val(res.data.password);
                $('#edit_message').text(res.msg);
                show_pop_div('user_edit');
               console.log("成功")
            }else{
                console.log("失败")
            }
        },
        error: () => {
            console.log('没有连接到服务器')
        }
    });
}

$('#user_edit > form').on('submit', function (e) {
    // 阻止默认提交事件
    e.preventDefault()
    // 采集用户信息
    var user_obj = get_edit_user_data();
    $.ajax({
        type: "post",
        url: "/user/add_or_update_user/",
        data:{"flag": "update","data":JSON.stringify(user_obj)},
        dataType: "json",
        success: res => {
            if (res.status) {
               $('#edit_message').text(res.msg);
               close_pop_div('user_edit');
               //刷新页面
               window.location.reload()
            }else{
                $('#edit_message').text(res.msg);
            }
        },
        error: () => {
            console.log('没有连接到服务器')
        }
    });
});

function get_edit_user_data() {
    var user_obj = {};
    user_obj['user_name'] = $('#edit_user_name').val();
    user_obj['user_id'] = $('#edit_user_id').val().toUpperCase();
    user_obj['phone']  = $('#edit_phone_num').val();
    user_obj['authority'] = $('#edit_authority').val();
    user_obj['password'] = $('#edit_user_password').val();
    return user_obj;
}

function get_add_user_data() {
    var user_obj = {};
    user_obj['user_name'] = $('#add_user_name').val();
    user_obj['user_id'] = $('#add_user_id').val().toUpperCase();
    user_obj['phone']  = $('#add_phone_num').val();
    user_obj['authority'] = $('#add_authority').val();
    user_obj['password'] = $('#add_user_password').val();
    return user_obj;
}

function clear_data(str) {
      $(str+'user_name').val('');
      $(str+'user_id').val('');
      $(str+'phone_num').val('');
      $(str+'authority').val('');
      $(str+'user_password').val('');
}

function del(obj) {
    del_user_id = $(obj).parent().parent().parent().find('.tb_user_id').text();
    $('#del_message').text("确定删除"+del_user_id+"?");
    show_pop_div('user_delete');
}

$('#del_btn').click(function (obj) {
    var user_id = del_user_id
     $.ajax({
        type: "post",
        url: "/user/delete_user/",
        data:{"user_id": user_id},
        dataType: "json",
        success: res => {
            if (res.status) {
               $('#del_message').text(res.msg);
               close_pop_div('user_delete');
               //刷新页面
               window.location.reload()
            }else{
                 $('#del_message').text(res.msg);
            }
        },
        error: () => {
            console.log('没有连接到服务器')
        }
    });
});


/****************** 搜索 ******************** start */
$('#btn_search').click(function () {
    // 點擊和回車搜索框
    search_function();
});

function search_function() {
    var key_word = $("#search_input").val();
    var url = '/user/user_manage/' + '?keyword=' + key_word;
    window.location.href = url;
}

$(document).keyup(function () {
    if ($("#search_input").is(":focus")) {
        var searching_input = $("#search_input").val();
        if (searching_input != "") {
            if (event.keyCode == 13) {
                search_function();
            }
        }
    }
});

/****************************搜索*************************************/

/***************************关闭添加框***************************************/
function close_add_div() {
    clear_data('#add_');
    close_pop_div('user_add')
}