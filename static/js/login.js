// 判断账号密码是否输入决定样式
$("#username").bind("input propertychange",function(event){
    $("#username").val() ? $("#icon_user").addClass('activate') : $("#icon_user").removeClass();
})

$("#password").bind("input propertychange",function(event){
    $("#password").val() ? $("#icon_pass").addClass('activate') : $("#icon_pass").removeClass();
})

// // 登录页面逻辑代码
// $('form').on('submit', function (e) {
//     // 阻止默认提交事件
//     e.preventDefault();
//     // 采集用户信息
//     const data = $('form').serialize();
//     // 格式化数据
//     let json_data_str = formToJson(data)
//     console.log(json_data_str);
//     json_data = {'data': json_data_str}
//     // 发送请求数据
//     // $.post('http://10.197.24.71:8888/index/machine_manage/', json_data, res => {console.log(res)})
//     $.ajax({
//         type: "post",
//         url: "/user/login/",
//         data: json_data,
//         dataType: "json",
//         success: res => {
//             if (res.status) {
//                 $('.login_box .message').css('visibility','visible')
//                 $('.login_box .message').text(res.msg)
//             }else{
//                 console.log('res.status:', res.status)
//                 console.log('res.msg:', res.msg);
//                 $('.login_box .message').css('visibility','visible')
//                 $('.login_box .message').text(res.msg)
//             }
//         },
//         error: () => {
//             console.log('没有连接到服务器')
//         }
//     });
// })