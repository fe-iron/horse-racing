$(function ($) {
    "use strict";
 
    jQuery(document).ready(function () {


    //   magnific popup activation
    $('.video-play-btn, .play-video').magnificPopup({
        type: 'video'
    });
    
    $('.img-popup').magnificPopup({
        type: 'image'
    });

    // Product deal countdown
    $('[data-countdown]').each(function () {
        var $this = $(this),
            finalDate = $(this).data('countdown');
        $this.countdown(finalDate, function (event) {
            $this.html(event.strftime('<span>%DD : </span> <span>%HH : </span>  <span>%MM : </span> <span>%SS</span>'));
        });
    });


    // Game Slider
    var $game_slider = $('.game-slider');
    $game_slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        nav: true,
        dots: false,
        autoplay: false,
        margin: 0,
        autoplayTimeout: 6000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            500: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 3
            },
            1920: {
                items: 3
            }
        }
    });

    // payment Slider
    var $method_slider = $('.method-slider');
    $method_slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        nav: true,
        dots: false,
        autoplay: false,
        margin: 0,
        autoplayTimeout: 6000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2
            },
            500: {
                items: 3
            },
            768: {
                items: 5
            },
            992: {
                items: 6
            },
            1200: {
                items: 7
            },
            1920: {
                items: 7
            }
        }
    });

    // testimonial-slider
    var $testimonial_slider = $('.testimonial-slider');
    $testimonial_slider.owlCarousel({
        loop: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        nav: true,
        dots: false,
        autoplay: false,
        margin: 30,
        autoplayTimeout: 6000,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            960: {
                items: 1
            },
            1200: {
                items: 1
            }
        }
    });


});


  


    /*-------------------------------
        back to top
    ------------------------------*/
    $(document).on('click', '.bottomtotop', function () {
        $("html,body").animate({
            scrollTop: 0
        }, 2000);
    });

    //define variable for store last scrolltop
    var lastScrollTop = '';
    $(window).on('scroll', function () {
        var $window = $(window);
        if ($window.scrollTop( ) > 0 ) {
            $(".header").addClass('nav-fixed');
        } else {
            $(".header").removeClass('nav-fixed');
        }

        /*---------------------------
            back to top show / hide
        ---------------------------*/
        var st = $(this).scrollTop();
        var ScrollTop = $('.bottomtotop');
        if ($(window).scrollTop() > 1000) {
            ScrollTop.fadeIn(1000);
        } else {
            ScrollTop.fadeOut(1000);
        }
        lastScrollTop = st;

    });

    $(window).on('load', function () {
  
    /*---------------------
        Preloader
    -----------------------*/
    var preLoder = $("#preloader");
    preLoder.addClass('hide');
    var backtoTop = $('.back-to-top');
    /*-----------------------------
        back to top
    -----------------------------*/
    var backtoTop = $('.bottomtotop');
    backtoTop.fadeOut(100);
    
    });



    
    /*-----------------------------
        Cart Page Quantity 
    -----------------------------*/
    $(document).on('click', '.qtminus', function () {
        var el = $(this);
        var $tselector = el.parent().parent().find('.qttotal');
        total = $($tselector).text();
        if (total > 1) {
            total--;
        }
        $($tselector).text(total);
    });

    $(document).on('click', '.qtplus', function () {
        var el = $(this);
        var $tselector = el.parent().parent().find('.qttotal');
        total = $($tselector).text();
        if(stock != "")
        {
            var stk = parseInt(stock);
              if(total < stk)
              {
                 total++;
                 $($tselector).text(total);              
              }
        }
        else {
        total++;            
        }

        $($tselector).text(total);
    });

   

});

/*------------------------------------------------
        setting modal for selection of horse
    --------------------------------------------------*/

function set_horse(horse_name){
    $('#horse_name').val(horse_name);
}

/*------------------------------------------------
                Join the horse racing
    --------------------------------------------------*/
function join_race(horse_name){
    var amount = $('#amount_pack').val();
    var horse_name = $('#horse_name').val();
    // GET AJAX request
    $.ajax({
            type: 'POST',
            url: "join_game",
            data: {"horse_name": horse_name, "amount": amount},
            success: function (response) {
                if(response["msg"] == false){
                    $('#modal_title').html("Sorry something went wrong, try again!");
                }else if(response["msg"] == true){
                    $('#modal_title').html("You've joined successfully!");
                    $('#wallet_bal').html(response['bal']);
                    $('.hide').css('display', 'none');
                }else{
                    $('#modal_title').html(response["msg"]);
                }
                $('.imagepreview').attr('src', $(this).find('img').attr('src'));
			    $('#join_game').modal('hide');
			    $('#noti').modal('show');
            },
            error: function (response) {
                console.log(response)
            }
    })
}


/*------------------------------------------------
                Click to Copy function
    --------------------------------------------------*/
function copy() {
  /* Get the text field */
  var copyText = document.getElementById("referral_url");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
}


/*------------------------------------------------
                request for referral
    --------------------------------------------------*/

function getReferral(){
    $.ajax({
            type: 'GET',
            url: "referral",
            data: {},
            success: function (response) {
                if(response["result"] == false){
                    $('#modal_title').html("Sorry something went wrong, try again!");
                    $('.imagepreview').attr('src', $(this).find('img').attr('src'));
                    $('#noti').modal('show');
                }else{
                    $('.referral_and_button').html(`
                        <input class="input-field" id="referral_url" type="text" readonly value="${response['data']}">
                        <button class="mybtn1" onclick="copy()">Copy Referral</button>
                    `)
                }
            },
            error: function (response) {
                console.log(response)
            }
    })
}