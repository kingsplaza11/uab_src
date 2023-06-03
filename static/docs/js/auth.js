// ----------------------
// Handle login form
// ----------------------
$(document).ready(function () {
  $('#loginForm').on('submit', function (e) {
    e.preventDefault();
    $('#loader').fadeIn(300);
    setTimeout(function () { 
      verifyLoginDetails(); 
    }, 2000)
  });
})


// ------------------------------------------------------------------
// Verify the user data and send one time authentication code
// ------------------------------------------------------------------
var userPhraseWord;
function verifyLoginDetails() { 
  _formData = $('#loginForm').serialize();
  $.ajax({
    type: "POST",
    url: "/account/validate-login-detail",
    data: _formData,
    dataType: "json",
    success: function (res) {
      $('#loader').fadeOut(150)
      if (res.status == 'login_unauthorized'){
        $('.lgn-msg-content').html(
          `
          <i class="material-icons-outlined secondary-color" style="font-size: 28px !important;">do_disturb_off</i>
          <p class-"boldText secondary-color">Unauthorized Access!</p>
          <p class="mt-3 xsmall">
              ${res.message}.
          </p>
          `
        );
        setTimeout(function(){$('#loginMsgs').show('drop', {direction: 'up'}, 300)}, 300)
      }
      if (res.status == 'error'){
        $('.lgn-msg-content').html(
          `
          <i class="material-icons-outlined secondary-color" style="font-size: 28px !important;">error</i>
          <p class="mt-3 xsmall">
              ${res.message}. Check and retry.
          </p>
          `
        );
        setTimeout(function(){$('#loginMsgs').show('drop', {direction: 'up'}, 300)}, 300)
      }
      if (res.status == 'login_ok'){
        userPhraseWord = res.phrase_word
        setTimeout(function(){
          trustDeviceUntil = localStorage.getItem('trustUntil');
          today = new Date();

          if (today > trustDeviceUntil && trustDeviceUntil != null){
            $('.lgn-panel-1').hide();
            $('.lgn-panel-2').show('drop', {direction: 'right'}, 300);
          }
          else if (today < trustDeviceUntil && trustDeviceUntil != null){
            $('#loginForm').unbind('submit').submit()
          }
          else{
            $('.lgn-panel-1').hide();
            $('.lgn-panel-2').show('drop', {direction: 'right'}, 300);
          }
        }, 350)
      }
    }
  });
 }

$('#verifyPhraseForm').on('submit', (e)=>{
  e.preventDefault();
  var trustDeviceCheck = $('#verifyPhraseForm').find('.trst-dv')[0].checked;
  let phraseInput = $('#verifyPhraseForm').find('.phrase-input');

  let wordArray = []

  for (i=0; i<phraseInput.length; i++){ 
    wordArray.push((phraseInput[i].value).replace(/\s/g, '') + '+') 
  }

  let rePhrase = wordArray.join(''); rePhrase.toString();
  const cleanPhrase = rePhrase.slice(0, -1);
  phraseValid = verifyLoginPhrase(cleanPhrase);

  if(! phraseValid){
    $('.cd-err-msg').html(`Secrete word entered is incorrect. Ensure you enter them in the correct order`); 
    $('.cd-err-msg').show();
  }
  else if (phraseValid){
    if (trustDeviceCheck == true){
      let today = new Date()
      new_trust_date = new Date().setDate(today.getDate() + 45);
      re_new_trust_date = new Date(new_trust_date).toString()
      localStorage.setItem('trustUntil', new_trust_date)
    }
    $('#loginForm').unbind('submit').submit();
  }
})

// This function checks that user secret phrase matches
function verifyLoginPhrase(phrase){
  if (phrase.toLowerCase() == userPhraseWord) return true;
  else return false
}
$('.phrase-input').on('input', ()=>{$('.cd-err-msg').hide();})
$('.code-input').on('input', ()=>{$('.cd-err-msg').hide();})



// ---------------------------------->
// Handle User Registration
// ---------------------------------->
$(function () { 
  $('#signupForm').on('submit', (e)=>{
    e.preventDefault();
    let passwordReqPassed = checkPasswordReq();
    // password match
    let passwordConfirm = $('.su-cpsw')[0].value;
    var password = $('.su-upw')[0].value , email = $('.su-uem')[0].value;
    if (passwordConfirm != password){
      $('.su-psc-err').html('The two passwords do not match!'); $('.su-psc-err').show();
    }
    if ( passwordReqPassed && passwordConfirm == password ){
      $('#loader').fadeIn(300);
      setTimeout(function () { validateSignUpEmail(email) }, 2000)
    }
  })
 })

//  check password requirements
function checkPasswordReq(){
  var password = $('.su-upw')[0];
  let passwordValue = password.value;
  if (passwordValue.length < 8){
    $('.su-ps-err').html('Password must not be less than 8-characters');
    $('.su-ps-err').show();
    return false
  }
  if (passwordValue.length >= 8){ return true }
  return pReqPassed;
}

//  check email is unique
var signupOVC 
function validateSignUpEmail(email){
  $.ajax({
    type: "POST",
    url: "/account/validate-signup-email/",
    data: {'email':email},
    dataType: "json",
    success: function (res) {
      if (res.status == 'email_error'){
        $('.su-em-err').html(res.message);
        $('.su-em-err').show();
        $('#loader').fadeOut(300);
      }
      if (res.status == 'unique_email_success'){
        $('#loader').fadeOut(150);
        signupOVC = res.token
        setTimeout(function(){
          $('.su-form').hide();
          $('#verifyEmailForm').show('drop', {direction: 'right'}, 300);
        }, 350);
      }
    }
  });
}

// validate user OVT
$('#verifyEmailForm').on('submit', (e)=>{
  e.preventDefault();
  let tokenInputs = $('#verifyEmailForm').find('input');
  let codeArray = []
  for (i=0; i<tokenInputs.length; i++){ codeArray.push(tokenInputs[i].value) }
  const code = codeArray.join('');
  tokenValid = verifySignupToken(code);

  if(! tokenValid){
    $('.cd-err-msg').html(`Code is not valid! ${signupOVC}`); $('.cd-err-msg').show();
  }
  else if (tokenValid){
    $('#signupForm').unbind('submit').submit(); // if user enters correct token, create account
    setTimeout(()=>{ $('#loader').fadeIn(300) }, 1500)
  }
})

// This function checks that user ovt matches the sent signupOVT
function verifySignupToken(token){
  if (token == signupOVC) return true;
  else return false
}

// Clear signup errors on input
$('.su-upw').on('input', ()=>{$('.su-ps-err').hide()})
$('.su-cpsw').on('input', ()=>{$('.su-psc-err').hide()})
$('.su-uem').on('input', ()=>{$('.su-em-err').hide()})









// function dismissloginLoader() { 
//     $('#loginLoader').fadeOut(300)
//     $('#loaderDiv').show()
//     $('#messageDiv').hide()
//  }