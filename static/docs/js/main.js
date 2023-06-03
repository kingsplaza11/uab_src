var dAmount = document.querySelector('#dAmount')

function openSideBarSm(){
    var toggleDrawer = document.querySelector('#toggleDrawer')
    
    $('#overlayDiv').show()
    $('#sideBarSm').show('slide', {direction: 'right'}, 400)
    toggleDrawer.onclick = hideSideBarSm
}

function hideSideBarSm(){
    var toggleDrawer = document.querySelector('#toggleDrawer')
    
    $('#overlayDiv').hide()
    $('#sideBarSm').hide('slide', {direction: 'right'}, 400)
    toggleDrawer.onclick = openSideBarSm
}

const dismissDialog = ()=>{
  $('.dialog').each(function(){
    $(this).hide('drop', {direction: 'up'}, 200);
  })
}

function setPaymentSystem(e){
    var paymentOptionValue = document.querySelector('#paymentOption')


    $('.pay-option-container').each(function(){
        $(this).removeClass('pay-option-container-active')

        checked = $(this).find('i')
        checked.removeClass('fi-rr-checkbox')
        checked.addClass('fi-rr-square')
    })
    $(e).addClass('pay-option-container-active')

    nowChecked = $(e).find('i')
    nowChecked.removeClass('fi-rr-square')
    nowChecked.addClass('fi-rr-checkbox')
    // ##
    paymentOptionValue.value = e.id
}


// verification code input
const inputElements = [...document.querySelectorAll('input.code-input')]

inputElements.forEach((ele,index)=>{
  ele.addEventListener('keydown',(e)=>{
    // if the keycode is backspace & the current field is empty
    // focus the input before the current. Then the event happens
    // which will clear the "before" input box.
    if(e.keyCode === 8 && e.target.value==='') inputElements[Math.max(0,index-1)].focus()
  })
  ele.addEventListener('input',(e)=>{
    const [first,...rest] = e.target.value
    e.target.value = first ?? '' // first will be undefined when backspace was entered, so set the input to ""
    const lastInputBox = index===inputElements.length-1
    const insertedContent = first!==undefined
    if(insertedContent && !lastInputBox) {
      // continue to input the rest of the string
      inputElements[index+1].focus()
      inputElements[index+1].value = rest.join('')
      inputElements[index+1].dispatchEvent(new Event('input'))
    }
  })
})

const dismissMessage = ()=>{
  $('#msg-notify').hide('slide', {direction: 'down'}, 300)
}


// *************>
const changeTheme = (e)=>{

  $('.themeIndicator').each(function(){
      $(this).removeClass('fa-check-circle')
  })

  $('#themeCss').prop('href', `/static/docs/css/${e.id}.css`)
  theme = $('#themeCss').prop('href')

  localStorage.setItem('theme', theme)
  $('#toggleDrawer').prop('src', `/static/assets/images/menu-bar-${e.id}.png`)

  // set Indicator

  indicator = $(e).find('span')[0]
  $(indicator).addClass('fa-check-circle')

  if (e.id == 'light'){
      $('.coinWidget1').hide()
      $('.coinWidget2').show()
  }
  else if (e.id == 'dark'){
      $('.coinWidget1').show()
      $('.coinWidget2').hide()
  }
}

$(function(){
  $(window).scroll(function () { 
    let scroll = $(window).scrollTop();
    let navMobile = $("#ind-mb-nv")[0];
    if (scroll >= 70) {
      $(navMobile).addClass('navMobileActiveIndex')
      // $(navLg).addClass('navMobileActiveIndex')
      $("#ind-mb-nv").find('.lY').removeClass('textColor2');
      $("#ind-mb-nv").find('.lX').removeClass('greyWhiteX');
      $('#lM').attr('src', '/static/assets/images/uab-logo.png')

      $('#toggleDrawer').html(`
      <div class="mt-3" style="width: 90%; height: 2.5px; background: #000; border-radius: 4px;"></div>
      <div class="mt-1" style="width: 90%; height: 2.5px; background: #000; border-radius: 4px;"></div>
      <div class="mt-1" style="width: 90%; height: 2.5px; background: #000; border-radius: 4px;"></div>
      `)

      // $("#db-dsktp-header").addClass("navbar-active");
      }
    else{
      $(navMobile).removeClass('navMobileActiveIndex')
      // $(navLg).removeClass('navMobileActiveIndex')
      $("#ind-mb-nv").find('.lY').addClass('textColor2');
      $("#ind-mb-nv").find('.lX').addClass('greyWhiteX');
      $('#lM').attr('src', '/static/assets/images/uab-logo-white.png')

      $('#toggleDrawer').html(`
      <div class="mt-3" style="width: 90%; height: 2.5px; background: #f6f1f1; border-radius: 4px;"></div>
      <div class="mt-1" style="width: 90%; height: 2.5px; background: #f6f1f1; border-radius: 4px;"></div>
      <div class="mt-1" style="width: 90%; height: 2.5px; background: #f6f1f1; border-radius: 4px;"></div>
      `)
    }
   })
})

// *******>
$('.dwrp-cont').scroll(function () {
  var scroll = $('.dwrp-cont').scrollTop();
  if (scroll >= 70) {
    let dbNavMobile = $("#dbNavMobile")[0];
      $(dbNavMobile).addClass("navMobileActive");
      $("#db-dsktp-header").addClass("navbar-active");

    }
  else{
      $(dbNavMobile).removeClass("navMobileActive");
      $("#db-dsktp-header").removeClass("navbar-active");
  }
});
// ******>

$(document).on('click', 'a[href^="#"]', function (event) {
  event.preventDefault();
  $('html, body').animate({
      scrollTop: $($.attr(this, 'href')).offset().top - 500
  }, 1000);
});



// ******>
function changeLang(e){
  $('.language-div').show('slide', {direction:'right'}, 400)

  icon = $(e).find('i')
  $(icon).removeClass('fi-rr-angle-small-right')
  $(icon).addClass('fi-rr-angle-small-left')

  $(e).attr('onclick', "closeChangeLang(this)")
}

function closeChangeLang(e){
  $('.language-div').hide('slide', {direction:'right'}, 400)

  icon = $(e).find('i')
  $(icon).addClass('fi-rr-angle-small-right')
  $(icon).removeClass('fi-rr-angle-small-left')

  $(e).attr('onclick', "changeLang(this)")
}
// lang Mobile
function showLangMobile(e){
  $('#langMobile').show('slide', {direction:'right'}, 200);
  $(e).attr('onclick', 'hideLangMobile(this)')
}
function hideLangMobile(e){
  $('#langMobile').hide('slide', {direction:'right'}, 200);
  $(e).attr('onclick', 'showLangMobile(this)')
}



$(function(){
  function greet(){
    const greeting = $('.greet-user');
    const hour = new Date().getHours();
    const welcomeTypes = ["Good morning", "Good afternoon", "Good evening"];
    let welcomeText = "";

    if (hour < 12) welcomeText = welcomeTypes[0];
    else if (hour < 18) welcomeText = welcomeTypes[1];
    else welcomeText = welcomeTypes[2];
    $(greeting).html(welcomeText);
  }
  greet();
})