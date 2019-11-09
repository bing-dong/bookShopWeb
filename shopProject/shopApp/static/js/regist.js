$(document).ready(function(){

    // 判断用户名是否填写
    $(":text").keyup(function(){
        var name = $(":text").val();
        if (name == ''){
            $("#span_in").text("请填写用户名");
            $("#span_in").val("").css("color","#ff0000");
        }
        else{
            $("#span_in").text("");
            $("#span_in").val("").css("color","black");
        }

        //若用户名为空则不能点注册按钮
        if (name == ''){
            $(":submit").attr("disabled","true");
        }
        else{
            $(":submit").removeAttr('disabled');
        }

        //用Ajax判断用户是否存在
        $.ajax({
            type: "get",
            url:"verifyUser",
            data:{
                user:name
            },
            success(data){
                if (data['state']=="false"){
                    $("#span_in").text("用户名已存在！");
                    $("#span_in").val("").css("color","#ff0000");
                }
            },
            error(){
                alert("ajax配置有错，请检查url与type是否正确");
            }
        });
    });

    // 当输入密码时，检测密码强度   并确定密码是否填写
    $(":password").keyup(function(){
    // $("#pwstrength").text($(":password").val().length);
    var password = $(":password").val();
    if (password == '')
    {
        $("#pwstrength").text("请填写密码");
        $("#pwstrength").val("").css("color","#ff0000");
    }
    else if (password.length < 6){
        $("#pwstrength").text("密码长度最少6位，且含有字母和数字");
        $("#pwstrength").val("").css("color","#ff0000");
        return;
    }

    var cnt_num = 0; //判断是否含有数字
    var cnt_char = 0; //判断是否含有字母
    var Regx = /[0-9]/;
    
    for (var i=0;i < password.length; i++){
        var c = password.charAt(i);
        // $("#pwstrength").append(c);
        if (Regx.test(c))
            cnt_num = 1;
        else
            cnt_char = 1;
    }

    if (!cnt_char && cnt_num){
        $("#pwstrength").text("需数字和字母混合！密码强度：弱");
        $("#pwstrength").val("").css("color","#ff0000");
    }
    else if (cnt_char && !cnt_num){
        $("#pwstrength").text("需字母和数字混合！密码强度：弱");
        $("#pwstrength").val("").css("color","#ff0000");
    }
    else if (cnt_char && cnt_num){
        $("#pwstrength").text("格式正确！密码强度：强");
        $("#pwstrength").val("").css("color","#0000ff");
    }

    //若密码为空则不能点击注册按钮
    if (password == ''){
        $(":submit").attr("disabled","true");
    }
    else{
        $(":submit").removeAttr('disabled');
    }

    });
    
});
