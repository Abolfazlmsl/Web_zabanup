// filterSelection("all") // Execute the function and show all columns
// function filterSelection(c) {
//   let x, i;
//   x = document.getElementsByClassName("column");
//   if (c === "all") c = "";
//   // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
//   for (i = 0; i < x.length; i++) {
//     w3RemoveClass(x[i], "show");
//     if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
//   }
// }
//
// // Show filtered elements
// function w3AddClass(element, name) {
//   let i, arr1, arr2;
//   arr1 = element.className.split(" ");
//   arr2 = name.split(" ");
//   for (i = 0; i < arr2.length; i++) {
//     if (arr1.indexOf(arr2[i]) === -1) {
//       element.className += " " + arr2[i];
//     }
//   }
// }

// // Hide elements that are not selected
// function w3RemoveClass(element, name) {
//   var i, arr1, arr2;
//   arr1 = element.className.split(" ");
//   arr2 = name.split(" ");
//   for (i = 0; i < arr2.length; i++) {
//     while (arr1.indexOf(arr2[i]) > -1) {
//       arr1.splice(arr1.indexOf(arr2[i]), 1);
//     }
//   }
//   element.className = arr1.join(" ");
// }
//
// // Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
$('.owl-carousel').owlCarousel({
    rtl:true,
    loop:true,
    margin:10,
    nav:true,
    // autoplay:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:4
        }
    }
});

function filterSelection(category){
    if(category === 'all'){
        $(".nature-box").fadeIn();
        $(".car-box").fadeIn();
        $(".people-box").fadeIn();
        $(".book-carousel").removeClass('d-none');
        $(".filtered-nature").addClass('d-none')
    }
    else if (category === 'nature') {
        $(".car-box").fadeOut();
        $(".people-box").fadeOut();
        $(".nature-box").fadeIn();
        $(".book-carousel").addClass('d-none');
        $(".filtered-nature").removeClass('d-none')
    } else if (category === 'car') {
        $(".car-box").fadeIn();
        $(".nature-box").fadeOut();
        $(".people-box").fadeOut();

    } else if (category === 'people') {
        $(".nature-box").fadeOut();
        $(".car-box").fadeOut();
        $(".people-box").fadeIn();
    }
}

$("#toggle-question-type").click(function () {
    $("#question-type-choices").toggle();
    let hasClass = $("#toggle-question-type").hasClass('rotate-down-sidebar');
    if (!hasClass){
        $("#toggle-question-type").addClass('rotate-down-sidebar');
    } else {
        $("#toggle-question-type").removeClass('rotate-down-sidebar');
    }

});
$("#toggle-passage-type").click(function () {
    $("#passage-type-choices").toggle()
    let hasClass = $("#toggle-passage-type").hasClass('rotate-down-sidebar');
    if (!hasClass){
        $("#toggle-passage-type").addClass('rotate-down-sidebar');
    } else {
        $("#toggle-passage-type").removeClass('rotate-down-sidebar');
    }
});
$("#toggle-cambridge-books").click(function () {
    $("#cambridge-book-choices").toggle()
    let hasClass = $("#toggle-cambridge-books").hasClass('rotate-down-sidebar');
    if (!hasClass){
        $("#toggle-cambridge-books").addClass('rotate-down-sidebar');
    } else {
        $("#toggle-cambridge-books").removeClass('rotate-down-sidebar');
    }
});