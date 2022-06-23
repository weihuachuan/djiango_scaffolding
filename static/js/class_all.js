
// 通用函数
/* 弹出DIV模态框相关代码，包含展开了关闭 */
function show_pop_div(div_id) {
    this_div = document.getElementById(div_id);
    this_div.style.display = "block";
//以下部分使整个页面至灰不可点击
    var procbg = document.createElement("div"); //首先创建一个div
    procbg.setAttribute("id", "mybg"); //定义该div的id
    procbg.style.background = "#00000099";
    procbg.style.width = "100%";
    procbg.style.height = "100%";
    procbg.style.position = "fixed";
    procbg.style.top = "0";
    procbg.style.left = "0";
    procbg.style.zIndex = "9";
    // procbg.style.opacity = "0.6";
    procbg.style.filter = "Alpha(opacity=70)";
    // 增加毛玻璃特效
    procbg.style.backdropFilter = 'blur(3px)';
//背景层加入页面
    document.body.appendChild(procbg);
    document.body.style.overflow = "hidden"; //取消滚动条
}
//关闭模态框
function close_pop_div(div_id) {
    this_div = document.getElementById(div_id);
    this_div.style.display = "none";
    document.body.style.overflow = "auto"; //恢复页面滚动条
    var body = document.getElementsByTagName("body");
    var mybg = document.getElementById("mybg");
    body[0].removeChild(mybg);
    $("#"+div_id+" .message").empty();
    $("#"+div_id+" input").val("");
}

// 将收集的form表单提交的字符串数据格式化成json字符串格式（可通过JSON.parse（）转化为对象）
function formToJson (data) {
    data=data.replace(/&/g,"\",\"");
    data=data.replace(/=/g,"\":\"");
    data="{\""+data+"\"}";
    data = JSON.parse(data);
    return data;
}

//定义serializeObject方法，序列化表单
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
}

// 设定时间方法
function showTime(clock){
    let now = new Date();
    let hour = now.getHours() < 10 ? `0${now.getHours()}` : now.getHours();
    let minu = now.getMinutes()< 10 ? `0${now.getMinutes()}` : now.getMinutes();
    let second = now.getSeconds() < 10 ? `0${now.getSeconds()}` : now.getSeconds();
    let time = `${hour}:${minu}:${second}`;
    clock.innerHTML = time;
}
// 获取需要设置的位置，初始化后设置每秒刷新一次。
var clock = document.getElementById("show_current_time");
showTime(clock)
window.setInterval("showTime(clock)",1000);



/****************** 当前日期 ******************** */
$(function () {
    var date = new Date();
    var today = date.getFullYear()+'/'+(date.getMonth()+1)+'/'+date.getDate();
    $(".date").text(today);
});


/****************** 获取cookie值 ********************* start */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/***********************登出按钮点击*********************************/
$('.log_out').click(function () {
   window.location.href =  '/user/logout/'
});

/***************获取页面头部信息*************************/
var token=$.cookie("token");
token = token.split('.');
var str = token[1];
var obj = JSON.parse(decodeURIComponent(escape(window.atob(str))));
var user_id = obj.user_id;
var user_name = obj.user_name;
const current_authority = obj.authority;
$('#head_user_name').text(user_name);
$('#head_user_id').text(user_id);
/*******************************************************/

/*********************ExcleExprot start*******************************/
function exportToExcel(div_id,FileName) {
    var table = $('#'+div_id);
        if (table && table.length) {
            $(table).table2excel({
                exclude: ".noExl",
                name: "Excel Document Name",
                filename: FileName + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
                fileext: ".xls",
                exclude_img: true,
                exclude_links: true,
                exclude_inputs: true,
                preserveColors: true,
                width: 100,
            });
        }
}
/************************ExcleExprot end*****************************/