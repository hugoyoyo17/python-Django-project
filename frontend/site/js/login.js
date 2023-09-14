$(function(){
  // 一般登入
$('#login_btn').click(function(){
  $.ajax({
    type:'post',
    url:baseUrl+'/v1/login/',
    dataType:'json',
    contentType:'application/json',
    data:JSON.stringify({
      'email':$('#email').val(),
      'password':$('#password').val()
    }),
    success:function(data){
      if(data.code==200){
        window.localStorage.clear();
        window.localStorage.setItem('miushop_token',data.data.token);
        window.localStorage.setItem('miushop_email',data.email);
        window.localStorage.setItem('miushop_username',data.username);
        window.localStorage.setItem('miushop_cartscount',data.carts_count)
        alert('登入成功');
        window.location.href='index.html'
      }else{
        alert(data.error);
      }
    }
  })
})



})
// GOOGLE第三方登入
function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
   var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
     return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));
 
   return JSON.parse(jsonPayload);
 };
 function handleCallback(response) {
    // console.log(response);
     const data = parseJwt(response.credential);
    //  console.log(data);
     var uid = data.sub;
     var username = data.name;
     var email = data.email;
     var accesstoken = response.credential
      $.ajax({
       type:'post',
       url:baseUrl+'/v1/users/google/user',
       dataType:'json',
       contentType:'application/json',
       data:JSON.stringify({
        uid:uid,
        username:username,
        email:email,
        accesstoken:accesstoken
       }),
       success:function(data){
        if(data.code==201){
          window.localStorage.setItem('miushop_token',data.data.token);
          window.localStorage.setItem('miushop_email',data.email);
          window.localStorage.setItem('miushop_username',data.username);
          window.localStorage.setItem('miushop_cartscount',data.carts_count);
            console.log('註冊成功')
            alert('註冊成功!');
            window.location.href='verify.html'
        }
        else if(data.code==200){
          window.localStorage.clear();
          window.localStorage.setItem('miushop_token',data.data.token);
          window.localStorage.setItem('miushop_email',data.email);
          window.localStorage.setItem('miushop_username',data.username);
          window.localStorage.setItem('miushop_cartscount',data.carts_count);
          alert('登入成功');
          window.location.href='index.html'
        }        
        else{
            alert(data.error);
        }
    }
     })
}



//  FB第三方登入
    window.fbAsyncInit = function() {
      FB.init({
        appId      : '<your_appId>', //從firebase中獲取
        cookie     : true,
        xfbml      : true,
        version    : 'v16.0'
      });
        
      FB.AppEvents.logPageView();   
      FB.getLoginStatus(function(response) {
    // statusChangeCallback(response);
});
    };
  
    (function(d, s, id){
       var js, fjs = d.getElementsByTagName(s)[0];
       if (d.getElementById(id)) {return;}
       js = d.createElement(s); js.id = id;
       js.src = "https://connect.facebook.net/zh-TW/sdk.js";
       fjs.parentNode.insertBefore(js, fjs);
     }(document, 'script', 'facebook-jssdk'));


     function testAPI() {                      // Testing Graph API after login.  See statusChangeCallback() for when this call is made.
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me?fields=name,email', function(response) {
      console.log('Successful login for: ' + response.name+response.email);
    //   document.getElementById('status').innerHTML =
    //     'Thanks for logging in, ' + response.name + '!';
    });
  }



  function statusChangeCallback(response){
    console.log(response)
    if(response.status=='connected'){
      // FB.login(function(response) {
      //   // handle the response
      //   }, {scope: 'public_profile,email',return_scopes: true});
      testAPI()
    }
}



    

// function checkLoginState() {
//   FB.getLoginStatus(function(response) {
//     statusChangeCallback(response);
//   });
// }


function checkLoginState() {
  FB.login(function(response) {
    if (response.authResponse) {
      // console.log('Welcome!  Fetching your information.... ');
      var uid = response.authResponse.userID;
      var accesstoken = response.authResponse.accessToken
      FB.api('/me?fields=name,email', function(response) {
        // console.log('Good to see you, ' + response.name + '.');
        var username = response.name;
        var email = response.email;
        $.ajax({
          type:'post',
          url:baseUrl+'/v1/users/fb/user',
          dataType:'json',
          contentType:'application/json',
          data:JSON.stringify({
          uid:uid,
          username:username,
          email:email,
          accesstoken:accesstoken
          }),
          success:function(data){
            if(data.code==201){
              window.localStorage.setItem('miushop_token',data.data.token);
              window.localStorage.setItem('miushop_email',data.email);
              window.localStorage.setItem('miushop_username',data.username);
              window.localStorage.setItem('miushop_cartscount',data.carts_count)
                console.log('註冊成功')
                alert('註冊成功!');
                window.location.href='verify.html'
            }
            else if(data.code==200){
              window.localStorage.clear();
              window.localStorage.setItem('miushop_token',data.data.token);
              window.localStorage.setItem('miushop_email',data.email);
              window.localStorage.setItem('miushop_username',data.username);
              window.localStorage.setItem('miushop_cartscount',data.carts_count)
              alert('登入成功');
              window.location.href='index.html'
            }        
            else{
                alert(data.error);
            }
        }
        })
      });


     } else {
      console.log('User cancelled login or did not fully authorize.');
     }
    }, {scope: 'public_profile,email',return_scopes: true});
    
}













