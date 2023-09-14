


$(function(){
    birthday()

})

// birthday
function birthday(){
    birthday_year();
    birthday_month();
    birthday_day();
}

function birthday_year(){
    var options ='';
    options+= '<select name="birthday_year" id="birthday_year">';
    options+='<option value="" id="option_start"></option>'
    for(var i =1923;i<=2020;i++){
        options+=`
        <option value="${i}">${i}</option>
        `
    }
    options+='</select>'
    $('#span_year').before(options)
}
function birthday_month(){
    var options ='';
    options+= '<select name="birthday_month" id="birthday_month">';
    options+='<option value="" id="option_start"></option>'
    for(var i =1;i<=12;i++){
        options+=`
        <option value="${i}">${i}</option>
        `
    }
    options+='</select>'
    $('#span_year').after(options)
}
function birthday_day(){
    var options ='';
    options+= '<select name="birthday_day" id="birthday_day">';
    options+='<option value="" id="option_start"></option>'
    for(var i =1;i<=31;i++){
        options+=`
        <option value="${i}">${i}</option>
        `
    }
    options+='</select>'
    $('#span_month').after(options)
}

function changeDay(){
    
}

function getDate(){
    var birY = $('#birthday_year').val();
    var birM = $('#birthday_month').val();
    var birD = $('#birthday_day').val()
    var birthdayDate = birY+'-'+birM+'-'+birD 
    if(birY=='' || birM=='' || birD==''){
        birthdayDate=''
    }
    return birthdayDate
}

// $('#sub_btn').click(function(){
//     console.log(123)
//     $.ajax({
//         type:'post',
//         url:'http://127.0.0.1:8000/v1/users/',
//         contentType:'application/json',
//         datatype:'json',
//         data:JSON.stringify({
//             'username':$('#username').val(),
//             'email':$('#email').val(),
//             'password':$('#password').val(),
//             'password_check':$('#password_check').val(),
//             'gender':$('#gender').val(),
//             'birthday':$('#birthday_year').val+'-'+$('#birthday_month').val+'-'+$('#birthday_day').val(),
//             'phone':$('#phone').val()
//         }),
//         success:function(data){
//             if(data.code==200){
//                 console.log('註冊成功')
//             }else{
//                 alert(data.error);
//             }
//         }
//     })
// })



