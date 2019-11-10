$(document).ready(function(){

    $("#btn_add_cart").click(function(){
        
        // 加入购物车 
        $.ajax({
            type: "get",
            url:"add_cart",
            data:{
            },
            success(data){
                if (data['state'] == "ok"){
                    $("#id_login").text(data["name"]);
                    // 登陆后显示用户名，禁止点击
                    $("#id_login").attr("disabled","true").css("pointer-events","none");
                }
                else{
                    $("#id_login").text("登陆");
                    // 退出后显示登陆，可以点击
                    $("#id_login").removeAttr('disabled');
                }
            },
            error(){
                alert("ajax配置有错，请检查url与type是否正确");
            }
        });
    });
});

