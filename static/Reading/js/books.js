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

getData()
function getData() {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/book/',
        type: "GET",
        dataType: "json",
        data: {

        },
        success: function (data) {
            // console.log(JSON.stringify(data));
            let books = data["book"];
            let categories = data["category"];
            let questionType = data["question_type"];
            let exam = data["exams"];

            //Categories information
            let categoryInfo = [];
            categories.map(item => {
                categoryInfo.push({
                    id: item["id"],
                    name: item["name"]
                })
            });

            categoryInfo.map(item => {
                $("#exam-categories").append(
                    `<button class="btn btn-sm btn-rounded" style="font-size: 12px" id="category-${item.id}" onclick="filterSelection('${item.name}')">${item.name}</button>`
                )
            });
            console.log(categoryInfo)
            activeBtn();

            // Books information
            let bookInfo = [];

            books.map(item => {
                bookInfo.push({
                    id: item["id"],
                    name: item["name"],
                    image: item["image"]
                })
            });
            bookInfo.map(item => {
                $("#cambridge-book-choices").append(
                    `<div class="form-check d-flex align-items-center my-2 p-0" style="direction: ltr">` +
                        `<input class="form-check-input" type="checkbox" id="book-${item.id}">` +
                        `<label class="form-check-label"  for="book-${item.id}" style="font-size: 16px; font-family: segoe">` +
                            `${item.name}` +
                        `</label>` +
                    `</div>`
                )
            });


            // Questions Type information
            let questionTypeInfo = [];

            questionType.map(item => {
                questionTypeInfo.push({
                    name: item["name"],
                    value: item["value"]
                });
            });
            console.log(questionTypeInfo.length);
            questionTypeInfo.map(item => {
                $("#question-type-choices").append(
                    `<div class="form-check d-flex align-items-center my-2 p-0" style="direction: ltr">` +
                        `<input class="form-check-input" type="checkbox" id="${item.name}">` +
                        `<label class="form-check-label"  for="${item.name}" style="font-size: 17px">` +
                            `${item.value}` +
                        `</label>` +
                    `</div>`
                )
            })

            // Exam information
            let examInfo = [];
            exam.map(item => {
                examInfo.push({
                    id: item["id"],
                    book: item["book"],
                    name: item["name"],
                    image: item["image"],
                    categories: item["categories"],
                    question_type: item["questions_type"]
                })
            });
            // console.log(examInfo);
            // let examsOfCategory = [];
            let examList = [];
            for (let i = 0; i < categoryInfo.length; i++) {
                let exam = [];
                for (let j = 0; j < examInfo.length; j++) {
                    for (let k = 0; k < examInfo[j].categories.length; k++) {
                        if (categoryInfo[i].name === examInfo[j].categories[k].name) {
                            exam.push(examInfo[j]);
                        }
                    }
                }
                examList.push({
                    category: categoryInfo[i].name,
                    exams: exam
                })
            }
            console.log(examList);
            examList.map(item => {
                $("#show-exams-container").append(
                    `<div class="col-12 ${item.category}-box">` +
                        `<b class="mr-2" style="font-size: 18px">${item.category}</b>` +
                        `<hr class="mt-1 mb-4">` +
                        `<div class="book-carousel" id="${item.category}">` +

                        `</div>` +
                        `<div class="row filtered-${item.category} d-none mx-0">` +
                            `<div class="${item.category}-filtered book-cart item mx-auto mx-md-2 my-1">` +

                            `</div>` +
                        `</div>` +
                    `</div>`
                );
                item.exams.map(itm => {
                    console.log(item.category)
                    $(`#${item.category}`).append(
                        `<div class="book-cart mx-auto item zoom">` +
                            `<div class="content">` +
                                `<img src="${itm.image}" alt="Mountains" style="width:100%">` +
                                `<h6 class="mt-3">${itm.name}</h6>` +
                                `<h6 class="mt-3">${itm.categories.name}</h6>` +
                                `<p>Description of ${itm.book}</p>` +
                            `</div>` +
                        `</div>`
                    )
                })
            })

//       `<div class="content">` +
//                                     `<img src="{% static 'Reading/Images/zabanup.jpg' %}" alt="Mountains" style="width:100%">` +
//                                     `<h4 class="mt-3">Book 1</h4>` +
//                                     `<p>Description of Book 1</p>` +
//                                 `</div>` +      //
            // console.log(examInfo)
            addOwl()
        }

    })
}

function activeBtn() {
    var btnContainer = document.getElementById("exam-categories");
    var btns = btnContainer.getElementsByClassName("btn");
    for (var i = 0; i < btns.length; i++) {
        console.log("btns: " + btns.length);
      btns[i].addEventListener("click", function(){
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
      });
    }
}

function addOwl() {
    $(".book-carousel").addClass('owl-carousel').addClass('owl-theme');
    $('.owl-carousel').owlCarousel({
        rtl:true,
        loop:false,
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
}