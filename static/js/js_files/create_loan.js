$(document).ready(function() {

    var loan_type = "None";
    var prov_type = "None";
    var operator_line = "None";
    var capital = parseInt($("#val-capital").val())
    var comaker = $("#val-comaker").val()
    var pending_loan = $("#val-pending").val()

    var providential = false;
    var emergency = false;
    var operator = false;
    var driver = false;
    var inline = false;
    var outline = false;
    var yescoll = false;
    var nocoll = false;

<<<<<<< HEAD
    // $("#btn-prov").click(function(){
    //     $(this).css('background-color','#888888');
    //     $("#btn-em").css('background-color','');

    //     providential = true;
    //     emergency = false;

    //     $("#prov-1").show();
    //     $("#prov-2").hide();
    //     $("#prov-3").hide();
    //     $("#prov-4").hide();
    //     $("#amount").hide();
    //     $("#final-submit").hide();
    //     loan_type = "Providential"
    // }); 

    // $("#btn-em").click(function(){
    //     // Add script to check existing balance
    //     $(this).css('background-color','#888888');
    //     $("#btn-prov").css('background-color','');

    //     providential = false;
    //     emergency = true;

    //     $("#prov-1").hide();
    //     $("#prov-2").hide();
    //     $("#prov-3").hide();
    //     $("#prov-4").hide();
    //     $("#amount").show();
    //     $("#final-submit").show();
    //     loan_type = "Emergency"
    // }); 

    // $("#btn-oper").click(function(){
    //     $(this).css('background-color','#888888');
    //     $("#btn-driv").css('background-color','');

    //     operator = true;
    //     driver = false;

    //     $("#prov-1").show();
    //     $("#prov-2").show();
    //     $("#prov-3").hide();
    //     $("#prov-4").hide();
    //     $("#amount").hide();
    //     $("#final-submit").hide();
    // }); 

    // $("#btn-driv").click(function(){
    //     $(this).css('background-color','#888888');
    //     $("#btn-oper").css('background-color','');

    //     operator = false;
    //     driver = true;

    //     $("#prov-1").show();
    //     $("#prov-2").hide();
    //     $("#prov-3").show();
    //     $("#prov-4").hide();
    //     $("#amount").hide();
    //     $("#final-submit").hide();
    // }); 
=======
    $("#btn-prov").click(function(){
        $(this).css('background-color','#888888');
        $("#btn-em").css('background-color','');

        providential = true;
        emergency = false;

        $("#prov-1").show();
        $("#prov-2").hide();
        $("#prov-3").hide();
        $("#prov-4").hide();
        $("#amount").hide();
        $("#final-submit").hide();
        loan_type = "Providential"
    }); 

    $("#btn-em").click(function(){
        // Add script to check existing balance
        $(this).css('background-color','#888888');
        $("#btn-prov").css('background-color','');

        providential = false;
        emergency = true;

        $("#prov-1").hide();
        $("#prov-2").hide();
        $("#prov-3").hide();
        $("#prov-4").hide();
        $("#amount").show();
        $("#final-submit").show();
        loan_type = "Emergency"
    }); 

    $("#btn-oper").click(function(){
        $(this).css('background-color','#888888');
        $("#btn-driv").css('background-color','');

        operator = true;
        driver = false;

        $("#prov-1").show();
        $("#prov-2").show();
        $("#prov-3").hide();
        $("#prov-4").hide();
        $("#amount").hide();
        $("#final-submit").hide();
    }); 

    $("#btn-driv").click(function(){
        $(this).css('background-color','#888888');
        $("#btn-oper").css('background-color','');

        operator = false;
        driver = true;

        $("#prov-1").show();
        $("#prov-2").hide();
        $("#prov-3").show();
        $("#prov-4").hide();
        $("#amount").hide();
        $("#final-submit").hide();
    }); 
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760

    $("#btn-inline").click(function(){

        $(this).css('background-color','#888888');
        $("#btn-outline").css('background-color','');

        inline = true;
        outline = false;

<<<<<<< HEAD
        // $("#prov-1").show();
        // $("#prov-2").show();
        // $("#prov-3").show();
        // $("#prov-4").hide();
        $("#nxt").show();
        // $("#amount").hide();
        // $("#final-submit").hide();
=======
        $("#prov-1").show();
        $("#prov-2").show();
        $("#prov-3").show();
        $("#prov-4").hide();
        $("#amount").hide();
        $("#final-submit").hide();
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760
    }); 
    $("#btn-outline").click(function(){
        // Add script to Check CBU
        $(this).css('background-color','#888888');
        $("#btn-inline").css('background-color','');

        inline = false;
        outline = true;

<<<<<<< HEAD
        // $("#prov-1").show();
        // $("#prov-2").show();
        // $("#prov-3").show();
        // $("#prov-4").hide();
        $("#nxt").show();
        // $("#amount").hide();
        // $("#final-submit").hide();
    });

=======
        $("#prov-1").show();
        $("#prov-2").show();
        $("#prov-3").show();
        $("#prov-4").hide();
        $("#amount").hide();
        $("#final-submit").hide();
    }); 
>>>>>>> 549418614833c8e5b4d8caf88e6746fdc1fb1760

    $("#btn-yescoll").click(function(){
        // Add script to Check CBU
        $(this).css('background-color','#888888');
        $("#btn-nocoll").css('background-color','');

        yescoll = true;
        nocoll = false;


        $("#prov-4").show();
        $("#amount").hide();
        $("#final-submit").hide();
    }); 
    $("#btn-nocoll").click(function(){
        // Add script to Check CBU
        $(this).css('background-color','#888888');
        $("#btn-yescoll").css('background-color','');

        yescoll = false;
        nocoll = true;

        $("#prov-4").hide();
        $("#amount").show();
        $("#final-submit").show();
    }); 

    $("#btn-collsubmit").click(function(){
        // Include script of submitting collateral information
        $("#amount").show();
        $("#final-submit").show();
    }); 

    $("#final-submit").click(function(){
        $("#error-message").hide()
        var loan_amount = parseInt($('#loan-amount').val())

        if (inline == true && operator == true && providential == true) {
            if (nocoll == true && loan_amount > capital) {
            $("#error-message").text("Inside Line without collateral is only allowed loans equal to its CBU")
            $("#error-message").show()
            } else if (loan_amount > 150000) {
            $("#error-message").text("Loans for Inside Line are only limited to 150,000")
            $("#error-message").show()}
        }

        if (outline == true && operator == true && providential == true) {
            if (nocoll == true && loan_amount > capital) {
            $("#error-message").text("Outside Line without collateral is only allowed loans equal to its CBU")
            $("#error-message").show()
            }
            else if (loan_amount > 60000) {
            $("#error-message").text("Loans for Outside Line are only limited to 60,000")
            $("#error-message").show()}
        }

        // INCLUDE DRIVER FILTERS
        // if (driver == true && providential == true) {
        //     if (nocoll == true && loan_amount > capital) {
        //     $("#error-message").text("Outside Line without collateral is only allowed loans equal to its CBU")
        //     $("#error-message").show()
        //     }
        //     else if (loan_amount > 60000) {
        //     $("#error-message").text("Loans for Outside Line are only limited to 60,000")
        //     $("#error-message").show()}
        // }

        if (emergency == true) {
            if (loan_amount > 5000) {
            $("#error-message").text("Emergency loans are only limited to 5,000")
            $("#error-message").show()}
        }

        if (!$("#error-message").is(':visible')) {
            var request = $.ajax({
                type: 'post',
                url: window.location.pathname,
                data: {'providential': providential,
                        'emergency': emergency,
                        'operator': operator,
                        'driver': driver,
                        'inline': inline,
                        'outline': outline,
                        'yescoll': yescoll,
                        'nocoll': nocoll,
                        'capital': capital,
                        'loan_amount': loan_amount,
                    },
                beforeSend: function(xhr, settings) {
                    function getCookie(name) {
                        var cookieValue = null;
                        if (document.cookie && document.cookie != '') {
                            var cookies = document.cookie.split(';');
                            for (var i = 0; i < cookies.length; i++) {
                                var cookie = jQuery.trim(cookies[i]);
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                    }
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                success: function(resp) {
                    window.location.href = "http://" + $(location).attr('host') + "/view-loan/" + resp;
                    console.log("Harroooo!")
                }
            });
        }
    }); 
});


// prov-1
// prov-2
// prov-3
// prov-4
// amount
// final-submit
