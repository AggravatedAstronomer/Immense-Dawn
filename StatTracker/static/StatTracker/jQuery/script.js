$(document).ready(function() {

    $('.contained-data-section').hide();
    $('.summoner-recent-accordion, .summoner-ranked-accordion').hide();
    $('#profile-error-3').hide();
    $('.contained-data-section').delay(500).fadeIn(500);
    $('.contained-profile, .error, p, td, h1, h2, h3, #index-sub-heading, h4, h5').not('#threat-header').not('#psych-header').not('#summoner-input-header').animate({
        opacity:0
    },0);
    $('p').delay(1000).animate ({
        opacity:1
        },1000);
    $('td').delay(1750).animate ({
        opacity:1
        },1000);
    $('h1').delay(500).animate({
        opacity:1
        },250);
    var indexHeader = $('#main-header').text();
    var indexHeaderExpansion = [":"," ","M","e","t","a","g","a","m","i","n","g"," ","E","v","o","l","v","e","d"];
    var j = 0;
    setTimeout(function() {
    letterSpawner();
    $('#main-header').animate({
        color: '#66FF66'
        },1000);
    }, 7000);
    setTimeout(function() {
    $('#main-header').animate({
        color: '#7789A9'
        },5000);
    }, 9000);
    function letterSpawner(){
        window.setTimeout(function(){
            $('#main-header').text(indexHeader + indexHeaderExpansion[j]);
            j++;
            indexHeader = $('#main-header').text();
            if (j < indexHeaderExpansion.length){
                letterSpawner();
            }
        }, 30);
    }
    $('h2:not(#recent-summoners-list-header, #ranked-game-summoners-list-header)').delay(500).animate({
        opacity:1
        },200);
    $('h3:not(#index-sub-heading, #effectiveness-rating)').delay(500).animate({
        opacity:1
        },200);
    $('#index-sub-heading').delay(2000).animate({
        opacity:1
        },1500);
    $('#effectiveness-rating').delay(2500).animate({
        opacity:1
        },1500);
    $('#pending-games').delay(3000).animate({
        opacity:1
        },1500);
    $('h4').delay(1500).animate({
        opacity:1
        },1000);
    $('h5:not(#pending-games)').delay(1500).animate({
        opacity:12
        },200);
    $('#summoner-input, .error').delay(750).animate({
        opacity:1
        },300);
    $('#threat-profile').delay(1000).animate({
        opacity:1
        },300);
    $('#psych-profile').delay(1250).animate({
        opacity:1
        },300);
    $('#recent-summoners-list-header').delay(1750).animate({
        opacity:1
        },200);
        $('.summoner-recent-accordion').accordion({collapsible: true, active: false});
    $('#ranked-game-summoners-list-header').delay(2250).animate({
        opacity:1
        },200);
        $('.summoner-ranked-accordion').accordion({collapsible: true, active: false});
    $('#recent-summoners-list-header').click(function(){
        $('#recent-summoners-list-header').toggleClass("glyphicon-chevron-right glyphicon-chevron-down");
        $('.summoner-recent-accordion').fadeToggle();
        $('#profile-error-3').fadeToggle();
        });
    $('#ranked-game-summoners-list-header').click(function(){
        $('#ranked-game-summoners-list-header').toggleClass("glyphicon-chevron-right glyphicon-chevron-down");
        $('.summoner-ranked-accordion').fadeToggle();
        $('#profile-error-3').fadeToggle();
        });
    $("p, td").not('.non-highlighting, .glyphicon, .summoner-accordion-info').mouseenter(function(){
        $(this).css("animation", "highlighting 1s infinite alternate")
        //$(this).css("background-color", "rgba(0,255,0,0.1)")
        //$(this).animate({
        //"background-color": "green"
            //}, 500);
        });
    $("p, td").not('.summoner-divider, .glyphicon').mouseleave(function(){
        $(this).css("animation", "None")
        //$(this).css("background-color", "rgba(0, 0, 0, 0.0)")
        //$(this).animate({
        //"background-color": "black"
            //}, 500);
        });
});