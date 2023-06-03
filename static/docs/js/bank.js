// When transfer pin is submitted perform actions
$(function(){
    $('#cashTransferForm').on('submit', (e)=>{
        e.preventDefault();
        $('#loader').fadeIn(300);
        fetchCashTransferDetails();
    })
})

// clear value
$('#trf-pin').on('input', ()=>{$('.pin-err-txt').hide()})


// var to be used in otp modal
var beneficiaryFullname, beneficiaryAccNo
// 
function fetchCashTransferDetails(){
    var trfProtocol = $('#trfProtocol').val();
    let beneficiaryAccountNumber = $('.ba-details')[0].value;
    var trfAmount = $('#trfAmount').val();
    if (trfProtocol == 'other-banks'){
        $('#otp-c-am').html(trfAmount); 
        $('#otp-c-name').html($('#accountName').val());
        $('#otp-c-accn').html(beneficiaryAccountNumber);
        setTimeout(()=>{
            $('#loader').fadeOut(200);
            $('#trfOtpModal').modal('show');
        }, 1500);
    }
    else{
        let token_csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            headers: {'X-CSRFToken' : token_csrf},
            type: "POST",
            url: "/core/fetch-transfer-data",
            data: {'beneficiary':beneficiaryAccountNumber},
            dataType: "json",
            success: function (res) {
                if (res.status == 'error'){
                    $('.c-trf-box').html(
                        `
                        <div class="p-3">
                            <div class="text-center">
                                <i class="material-icons-outlined secondary-color d-block mb-2" style="font-size:28px !important">error</i>
                                <span>
                                    <b>Request Aborted!</b>
                                </span>
                            </div>
                        </div>
                        <div class="white-bg2 add-radius-2 p-3">
                            <p class="xsmall m-0 mt-4 text-center">
                                ${res.message}
                            </p>
                            <div class="my-3 text-center">
                                <button class="Btn xsmall px-5 fit-content" data-dismiss="modal">Dismiss</button>
                            </div>
                        </div>
                        `
                    )
                    setTimeout(()=>{
                        $('#loader').fadeOut(200);
                        $('#confirmTransfer').modal('show');
                    }, 1500)
                }
                if (res.status == 'ok'){
                    $('#otp-c-am').html(trfAmount); 
                    $('#otp-c-name').html(res.beneficiary_name);
                    $('#otp-c-accn').html(res.beneficiary_acc_no);
                    $('.c-trf-box').html(
                        `
                        <div class="text-center py-1">
                            <p class="xsmall primary-color roboto boldText m-0 mt-2">Confirm Cash Transfer</p>
                            <small class="greyWhite xsmall2">Please check that the data below is correct</small>
                        </div>
                        <div class="mt-2 white-bg2 p-4 add-radius-2">
                            <div class="form-group">
                                <label class="xsmall">Total Amount - USD</label>
                                <input type="number" name="" class="form-input  boldText" value="${trfAmount}">
                            </div>
                            <div class="form-group">
                                <label class="xsmall boldText roboto">From*</label>
                                <select name="" class="form-input p-0 pl-3">
                                    <option>${res.user_fullname}</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="xsmall boldText roboto">To*</label>
                                <select name="" class="form-input p-0 pl-3">
                                    <option>${res.beneficiary_name} - ${res.beneficiary_acc_no}</option>
                                </select>
                            </div>
                            <div class="mt-4">
                                <button type="button" class="btn-outline py-2 fit-content px-4 border textColor" data-dismiss="modal">Cancel</button>
                                <button class="Btn py-2 fit-content px-4 border ml-3" onclick="openPinModal()">Continue</button>
                            </div>
                        </div>
                        `
                    )
                    setTimeout(()=>{
                        $('#loader').fadeOut(200);
                        $('#confirmTransfer').modal('show');
                    }, 1500)
                    // beneficiaryFullname = res.beneficiary_name; beneficiaryAccNo = res.beneficiary_acc_no
                }
            }
        });
    }
}


function checkBalLimit(e, balance){
    $('.amt-err-txt').hide();
    var userBalance = parseFloat(balance), amountEntered = parseFloat(e.value);
    let subBtn = $('#cashTransferForm').find('button')[0];
    $(subBtn).attr('disabled', true);
    if (amountEntered > userBalance && amountEntered != 0){
        $('.amt-err-txt').html('You do not have sufficient fund!');
        $('.amt-err-txt').show();
        $(subBtn).attr('disabled', true);
    }
    if(amountEntered == 0){
        $('.amt-err-txt').html('Please enter a valid amount!');
        $('.amt-err-txt').show();
        $(subBtn).attr('disabled', true);
    }
    else if(amountEntered <= userBalance && amountEntered != 0){
        $(subBtn).attr('disabled', false);
    }
}


function openPinModal() {
    $('#confirmTransfer').modal('hide'); 
    $('#loader').fadeIn(300);
    setTimeout(()=>{
        $('#loader').fadeOut(200);
        $('#trfOtpModal').modal('show');
    }, 1500)
}


$(function () {
    $('#confirmTrfForm').on('submit', (e) => {
        e.preventDefault();
        let pin = $('#trf-pin').val();
        $('#loader').fadeIn(300);
        setTimeout(() => {
            $.ajax({
                type: "POST",
                url: "/core/validate-transfer-pin",
                data: { 'trf-pin': pin },
                dataType: "json",
                success: function (res) {
                    if (res.status == 'success') {
                        $('#cashTransferForm').unbind('submit').submit();
                        $('#loader').fadeOut(200);
                    }
                    if (res.status == 'error') {
                        $('#loader').fadeOut(150);
                        $('.pin-err-txt').html('The PIN you entered is incorrect');
                        $('.pin-err-txt').show();
                    }
                }
            });
        }, 1500)
    })
})
