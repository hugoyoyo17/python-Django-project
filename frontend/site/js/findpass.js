$(function(){
    $('#send_verify').click(function(){
        $.ajax({
          type:'post',
          url:baseUrl+'/v1/users/password/get_verify',
          contentType:'application/json',
          dataType:'json',
          data:JSON.stringify({
            'email':$('#email').val()
          }),
          success:function(data){
            if(data.code==200){
              alert(data.data);
              $('#email').attr({'disabled':'disabled'});
              $('#label_verify').show();
              $('#verify').show();
              $('#check_verify').show();
    
            }else{
              alert(data.error);
            }
          }
        })
      })
    
      $('#check_verify').click(function(){
        $.ajax({
          type:'post',
          url:baseUrl+'/v1/users/password/check_verify',
          contentType:'application/json',
          dataType:'json',
          data:JSON.stringify({
            'email':$('#email').val(),
            'verify':$('#verify').val()
          }),
          success:function(data){
            if(data.code==200){
              alert(data.data);
              $('#label_email').hide();
              $('#email').hide();
              $('#send_verify').hide();
              $('#label_verify').hide();
              $('#verify').hide();
              $('#check_verify').hide();
              $('.displayN').removeClass('displayN');
            }else{
              alert(data.error)
            }
          }
        })
      })
    
      $('#pass_update').click(function(){
        $.ajax({
          type:'post',
          url:baseUrl+'/v1/users/password/newpass',
          contentType:'application/json',
          dataType:'json',
          data:JSON.stringify({
            'email':$('#email').val(),
            'new_pass':$('#newpass').val(),
            'new_pass_check':$('#newpass_check').val()
          }),
          success:function(data){
            if(data.code==200){
              alert(data.data);
              window.location.href='login.html'
            }else if(data.code==10318){
              alert(data.error);
              window.location.reload();
            }else{
              alert(data.error);
            }
          }
        })
      })
})