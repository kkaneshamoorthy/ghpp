//jQuery to collapse the navbar on scroll
$(window).scroll(function() {

    var wScroll = $(this).scrollTop();

    if (wScroll >= 100) {
        $('#menuBar').css({
            'transform' : 'translate(0px, ' + wScroll / 8.5 + '%)'
        });
    }

    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});



function stepnext(n){

    if(n != 0){
		//$(".stepwizard-row a").switchClass('btn-primary','btn-default');
        $(".stepwizard-row a").removeClass('btn-primary');
        $(".stepwizard-row a").addClass('btn-default');
		$('.stepwizard a[href="#step-'+n+'"]').tab('show');
		//$('.stepwizard-row a[href="#step-'+n+'"]').switchClass('btn-default','btn-primary');
        $('.stepwizard-row a[href="#step-'+n+'"]').removeClass('btn-default');
        $('.stepwizard-row a[href="#step-'+n+'"]').addClass('btn-primary');
    }
}
stepnext(1);
