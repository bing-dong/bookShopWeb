$(document).ready(function(){
    $('.Select').click(function(){
        var tr = $(this).closest("tr");
        var name = tr.find("td:eq(0)").text();
        // alert(name);
        $.ajax({
        type: "get",
        url:"cart_del",
        data:{
            book_name:name
        },
        success(data){
            if(data['state'] == 'ok'){
                location.reload(true);
            }
        },
        error(){
            alert("ajax配置有错，请检查url与type是否正确");
        }
    });
    });
});