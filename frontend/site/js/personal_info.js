var email = window.localStorage.getItem('miushop_email')


$(function (){
   LoadSelectorInfo()
      loadUserList();
  

  // 點擊使地址表單縮回/下拉
$('.address_info_div').click(function(){
  var id = $(this).data('uid')
  // console.log(id)
  $('.address_slider_open:eq('+(id-1)+')').toggleClass('address_slider_close')
  $('.address_slider_div:eq('+(id-1)+')').slideToggle('slow')
})


  // 點擊新增地址表單 最多五次
  $('.add_address').click(function(){
    var j=0
    while(true){
      // console.log(j)
      if(j>5){
        alert('送貨地址最多上限為五個')
        break
      }
      if($('.address_edit_box:eq('+j+')').css('display')=='none'){
        $('.address_edit_box:eq('+j+')').show()
        break
      }else{
        j+=1
      }
    }
})

// 地址表單的收件人輸入 使用自執行函數讓內部函數i與外部函數相同
for(var i=1;i<=5;i++){
// console.log(i);
$('#address_username_'+i).on('input',(function(index){
  return function(){
    var input = $(this).val();
    // console.log(input);
    // console.log(index);
    $('.address_info:eq('+(index-1)+')').html(input+'-');
  };
})(i));
}

//地址表單地址輸入 
for(var i=1;i<=5;i++){
$('#address_address_'+i).on('input',(function(index){
  return function(){
    var input = $(this).val();
    // console.log(input);
    // console.log(index);
    $('.address_info_address:eq('+(index-1)+')').html(input);
  };
})(i));
}

// 地址表單縣市選擇與顯示
for(var i=1;i<=5;i++){
$('.county:eq('+(i-1)+')').change((function(index){
  return function(){
    var input = $(this).val();
    // console.log(input);
    // console.log(index);
    if(input==''){
      // console.log('emp')
      html='-'
      $('.address_info_district:eq('+(index-1)+')').html(html)
    }
    $('.address_info_city:eq('+(index-1)+')').html(input+'');
    var thisdis = $(this).css('display')
    var cityhtml = $('.address_info_city:eq('+(index-1)+')').html()
    console.log(thisdis,cityhtml)
    if(thisdis=='inline-block'){
      console.log(1);
      if(cityhtml=='-'){
        window.location.reload()
      }
    }
  };
})(i));
}

// 地址表單區選擇與顯示
for(var i=1;i<=5;i++){
$('.district:eq('+(i-1)+')').change((function(index){
  return function(){
    var input = $(this).val();
    // console.log(input);
    // console.log(index);
    if(input==''){
      $('.address_info_district:eq('+(index-1)+')').html(input+'-') 
    }
    $('.address_info_district:eq('+(index-1)+')').html('-'+input+'-');
  };
})(i));
}



// 刪除鍵綁定 如果id存在刪除該id地址 否則隱藏地址表單
for(var i=1;i<=5;i++){
$('.delete_address_btn:eq('+(i-1)+')').on('click',(function(index){
return function(){
var id = $(this).data('uid');
// console.log(id);
if(id){
  del(id);
}else{
  // console.log(index)
  $('.address_edit_box:eq('+(index-1)+')').hide();
}
}
})(i));
}
// 取消鍵按鈕 重新get一次返回默認值
$('#cancel_btn').click(function(){
  window.location.reload()
loadUserList();
})

$('.get_verify').click(function(){
$.ajax({
    type:'get',
    url:baseUrl+'/v1/users/'+email+'/verify',
    beforeSend:function(request){
      request.setRequestHeader('authorization',localStorage.getItem('miushop_token'))
    },
    success:function(data){
      if(data.code==403){
        alert('用戶認證已過期，請重新登入')
            window.localStorage.removeItem('miushop_username');
            window.localStorage.removeItem('miushop_email');
            window.localStorage.removeItem('miushop_token');
            window.localStorage.removeItem('miushop_cartscount');
            window.location.href='login.html'
      }
      if(data.code==200){
        alert('發送成功')
      }else{
        alert(data.error)
      }
    }
    })
  })

$('#update_btn').click(function(){
var birthdayDate = ''
// 判斷使用者生日是否存在 不存在跳出年月日span讓使用者選填
if($('#birthday_exist').css('display')=='none'){
   birthdayDate = getDatePL();
}else{
   birthdayDate = $('#birthday_exist').val();
}
// var address_list = getAddress()
// var receiver_list = getReceiver()
// var receiver_phone_list = getReceiverPhone()
// var id_list = getId() 
var addressinfo_list = getAddressInfo()
console.log(addressinfo_list)
// console.log(address_list,receiver_list,receiver_phone_list,id_list)
$.ajax({
  type:'put',
  url:baseUrl+'/v1/users/'+email+'/address',
  contentType:'application/json',
  dataType:'json',
  data:JSON.stringify({
    'username':$('#username').val(),
    'email':$('#email').val(),
    'phone':$('#phone').val(),
    'password':$('#password').val(),
    'gender':$('#gender').val(),
    'birthday':birthdayDate,
    // 'receiver':receiver_list,
    // 'receiver_phone':receiver_phone_list,
    // 'address':address_list,
    // 'address_id':id_list,
    'addressinfo_list':addressinfo_list
  }),
  beforeSend:function(request){
    request.setRequestHeader('authorization',localStorage.getItem('miushop_token'))
  },
  success:function(data){
    if(data.code==200){
      alert('更新成功');
      window.location.reload();
    }else{
      alert(data.error)
    }
  }
})
})

$('.log_out').click(function(){
    window.localStorage.removeItem('miushop_username');
    window.localStorage.removeItem('miushop_token');
    window.localStorage.removeItem('miushop_email');
    window.localStorage.removeItem('miushop_cartscount')
    alert('退出登入');
    window.location.href='login.html'
    })


})

function loadUserList(){
  $.ajax({
    type:'get',
    url:baseUrl+'/v1/users/'+email+'/address',
    beforeSend:function(request){
      request.setRequestHeader('authorization',localStorage.getItem('miushop_token'))
    },
    async:false,
    success:function(data){
      if(data.code==403){
        alert('用戶認證已過期，請重新登入')
            window.localStorage.removeItem('miushop_username');
            window.localStorage.removeItem('miushop_email');
            window.localStorage.removeItem('miushop_token');
            window.localStorage.removeItem('miushop_cartscount');
            window.location.href='login.html'
      }
      if(data.code==200){
        var userList = data.userlist;
        var addressList = data.addresslist
        console.log("userList",userList);
        console.log("addressList",addressList);
        $('#username').val(userList.username);
        $('#email').val(userList.email).attr('disabled','disabled');
        $('#phone').val(userList.phone);
        if(userList.password=='exist'){
          $('#password').hide();
        }else{
          $('.change_pass').hide();
        }
        if(userList.gender=='M'){
          $('#gender').val(1)
        }
        else if(userList.gender=='W'){
          $('#gender').val(2)
        }
        else{
          $('#gender').val(3)
        }
        if(userList.birthday === null){
            // console.log(1)
            $('#birthday_exist').hide();

        }else{
            // console.log(2)
            $('.birthday_select').hide(); 
            $('#birthday_exist').val(userList.birthday);
        }
        $('.permission_name').text(userList.permission_name)
        if(userList.is_active){
          $('.person_active').text('用戶狀態--已驗證')
        }else{
          $('.person_active').text('用戶狀態--尚未驗證')
        }
        var i = 1;
        $('.address_edit_box').hide()
        for(var addr of addressList){
          $('.address_edit_box:eq('+(i-1)+')').show();

          // console.log(county,district)
          $('#address_username_'+i).val(addr.receiver);
          $('#address_phone_'+i).val(addr.receiver_phone);
          $('.county:eq('+(i-1)+')').attr('data-value',addr.county);
          if($('.county:eq('+(i-1)+')')){
            $('.district:eq('+(i-1)+')').attr('data-value',addr.district);
          }
          $('.address_info:eq('+(i-1)+')').html(addr.receiver+'-');
          $('.address_info_address:eq('+(i-1)+')').html(addr.road)
          $('#address_address_'+i).val(addr.road);
          $('.delete_address_btn:eq('+(i-1)+')').attr('data-uid',addr.id);
          var d = $('.address_info_city:eq('+(i-1)+')').html()
          // console.log("addressInfo ",d)
          console.log(d)
          if(d=='-'){
            setTimeout(
              console.log("addressInfo ",d)
              ,4000);
          }
          i+=1;
        }
      }else{
        alert(data.error)
      }
    }
  })
}

//   function getAddress(){
//     var address_list = []
//     for(var i=1;i<=5;i++){
//       var county = $('.county:eq('+(i-1)+')').val();
//       var district = $('.district:eq('+(i-1)+')').val();
//       var address_address = $('#address_address_'+i).val();
//       var address = county+'-'+district+'-'+address_address 
//       // if($('.address_edit_box:eq('+(i-1)+')').css('display')=='block'){
// // ******************************************
//       // }
//       if(county=='' || district=='' || address_address==''){
//         address=''
//       }
//       address_list.push(address)
//     }
//     return address_list
//   }
//   function getReceiver(){
//     var receiver_list = []
//     for(var i=1;i<=5;i++){
//     var receiver = $('#address_username_'+i).val();
//     receiver_list.push(receiver);
//   }
//   return receiver_list
// }

//   function getReceiverPhone(){
//     var receiver_phone_list = []
//     for(var i=1;i<=5;i++){
//     var receiver_phone = $('#address_phone_'+i).val();
//     receiver_phone_list.push(receiver_phone);
//   }
//   return receiver_phone_list
// }
// function getId(){
//     var id_list = []
//     for(var i=1;i<=5;i++){
//     var id = $('.delete_address_btn:eq('+(i-1)+')').attr('data-uid');
//     id_list.push(id);
//   }
//   return id_list
// }

function getAddressInfo(){
var addressinfo_list = []
for(var i=1;i<=5;i++){
  if($('.address_edit_box:eq('+(i-1)+')').css('display')=='none'){
    continue;
  }
  var addressinfo = [];
  var receiver = $('#address_username_'+i).val();
  var receiver_phone = $('#address_phone_'+i).val();
  var address_id = $('.delete_address_btn:eq('+(i-1)+')').attr('data-uid');
  var county = $('.county:eq('+(i-1)+')').val();
  var district = $('.district:eq('+(i-1)+')').val();
  var address_address = $('#address_address_'+i).val();
  var address = county+'-'+district+'-'+address_address;
  if(county=='' || district=='' || address_address==''){
      address=''
    }
  addressinfo.push(receiver,receiver_phone,address,address_id)
  addressinfo_list.push(addressinfo)
}
return addressinfo_list
}

function del(id){
$.ajax({
  type:'delete',
  url:baseUrl+'/v1/users/'+email+'/address',
  contentType:'application/json',
  dataType:'json',
  data:JSON.stringify({id,email}),
  beforeSend:function(request){
    request.setRequestHeader('authorization',window.localStorage.getItem('miushop_token'))
  },
  success:function(data){
    if(data.code==200){
      alert('刪除成功');
      window.location.reload();
    }else{
      alert(data.error);
    }
  }
})
}

function getDatePL(){
  var birY = $('#birthday_year').val();
  var birM = $('#birthday_month').val();
  var birD = $('#birthday_day').val()
  var birthdayDate = birY+'-'+birM+'-'+birD 
  if(birY=='' && birM=='' && birD==''){
    console.log(1)
      birthdayDate=''
  }
  return birthdayDate
}

async function LoadSelectorInfo () {
  console.log("LoadSelectorInfo")
new TwCitySelector({
  el: '.address_selecter1',
  elCounty: '.county', // 在 el 裡查找 element
  elDistrict: '.district', // 在 el 裡查找 element
  elZipcode: '.zipcode' // 在 el 裡查找 element
});
new TwCitySelector({
  el: '.address_selecter2',
  elCounty: '.county', // 在 el 裡查找 element
  elDistrict: '.district', // 在 el 裡查找 element
  elZipcode: '.zipcode' // 在 el 裡查找 element
});
new TwCitySelector({
  el: '.address_selecter3',
  elCounty: '.county', // 在 el 裡查找 element
  elDistrict: '.district', // 在 el 裡查找 element
  elZipcode: '.zipcode' // 在 el 裡查找 element
});
new TwCitySelector({
  el: '.address_selecter4',
  elCounty: '.county', // 在 el 裡查找 element
  elDistrict: '.district', // 在 el 裡查找 element
  elZipcode: '.zipcode' // 在 el 裡查找 element
});
new TwCitySelector({
  el: '.address_selecter5',
  elCounty: '.county', // 在 el 裡查找 element
  elDistrict: '.district', // 在 el 裡查找 element
  elZipcode: '.zipcode' // 在 el 裡查找 element
});
}
