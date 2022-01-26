if (document.getElementById('landing')) {
    $('#letters-carousel').slick({
        slidesToShow: 2,
        autoplay: true,
        centerMode: true,
        focusOnSelect: true,
        prevArrow: null,
        nextArrow: null,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                },
            },
        ],
    });
}
