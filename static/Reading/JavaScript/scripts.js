$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

setTimeout(() => {
    let width = window.matchMedia("(max-width: 992px)");
    let footer = $('#footer');
    let arrow = $('#arrow-self');
    let section = $('#section');
    if(width.matches){
        if(footer.css('height') === '256px'){
            footer.css('bottom', '-200px');
            arrow.removeClass('fa-arrow-down').addClass('fa-arrow-up');
            section.css('bottom', '56px');
        }
    }
    else {
        if(footer.css('height') === '156px'){
            footer.css('bottom', '-100px');
            arrow.removeClass('fa-arrow-down').addClass('fa-arrow-up');
            section.css('bottom', '56px');
        }
    }
}, 2000);
$('#toggler').on('click', function () {
   let nav = $('#options');
   let toggler = $('#toggler-icon');
   if(nav.css('right') === '0px')
   {
       nav.css('right', '-240px');
       toggler.removeClass('fa-times').addClass('fa-bars');
   } else {
       nav.css('right', '0px');
       toggler.removeClass('fa-bars').addClass('fa-times');
   }
});
$(document).on('click', "#question-palette h5, #arrow-self", function () {
    let width = window.matchMedia("(max-width: 992px)");

    let footer = $('#footer');
    let arrow = $('#arrow-self');
    let section = $('#section');
    if(width.matches) {
        switch (footer.css('bottom')) {
            case '0px':
            footer.css('bottom', '-200px');
            arrow.removeClass('fa-arrow-down').addClass('fa-arrow-up');
            section.css('bottom', '56px');
            break;
            case '-200px':
                footer.css('bottom', '0px');
                arrow.removeClass('fa-arrow-up').addClass('fa-arrow-down');
                section.css('bottom', '256px');
                break;
            }
    }
    else {
        switch (footer.css('bottom')) {
            case '-100px':
                footer.css('bottom', '0px');
                arrow.removeClass('fa-arrow-up').addClass('fa-arrow-down');
                section.css('bottom', '156px');
                break;
            case '0px':
                footer.css('bottom', '-100px');
                arrow.removeClass('fa-arrow-down').addClass('fa-arrow-up');
                section.css('bottom', '56px');
                break;
        }
    }
});

$('#test-info-btn').on('click', function () {
    let header = $('#header');
    let smallLogo = $('#small-logo');
    let testInfoIcon = $('#test-info-icon');
    switch (header.css('top')) {
        case '-120px':
            header.css('top', '0px');
            testInfoIcon.removeClass('fa-arrow-down').addClass('fa-arrow-up');
            setTimeout(() => smallLogo.removeClass('d-lg-block'), 350);

            break;
        case '0px':
            header.css('top', '-120px');
            setTimeout(() => smallLogo.addClass('d-lg-block'), 350);

            testInfoIcon.removeClass('fa-arrow-up').addClass('fa-arrow-down');
            break;
    }
});

/* Submit the exam */
$(document).on('click', "#submit-button, #small-submit-button", function () {
   let submitFakeButton = $('#submit-fake-button');
   submitFakeButton.removeClass('btn-danger').addClass('btn-dark');
   submitFakeButton.click()
});

