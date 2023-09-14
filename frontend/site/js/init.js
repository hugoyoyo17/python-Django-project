// 本地测试django_URL
baseUrl="http://127.0.0.1:8000"

$(function(){
var loginName = window.localStorage.getItem('miushop_username')
if(loginName){
    // console.log(loginName)
  $('#my_login').html(loginName).attr('href','personal_info.html')
}  
  var count = window.localStorage.getItem('miushop_cartscount')
  // console.log(count)
  if(count){
    $('.my_car_count').text(count)
  }
  else if(count>9){
    $('.my_car_count').text('9+')
  }
  else{
    $('.my_car_count').text(0)
  }
})
