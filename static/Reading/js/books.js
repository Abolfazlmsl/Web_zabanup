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

getData();

function getData() {
    $(".book-page-loader").removeClass('d-none').addClass('d-flex');
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

            // Fill the category buttons in top of the page;
            categoryInfo.map(item => {
                $("#exam-categories").append(
                    `<button class="btn btn-sm btn-rounded select-category" style="font-size: 12px" id="category-${item.id}" onclick="filtering()">${item.name}</button>`
                )
            });

            //Active selected category button
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

            // Fill the books filter in the sidebar
            bookInfo.map(item => {
                $("#cambridge-book-choices").append(
                    `<div class="form-check d-flex align-items-center my-2 p-0" style="direction: ltr">` +
                        `<input class="form-check-input book-name-item" type="checkbox" id="${item.id}" onclick="filtering()">` +
                        `<label class="form-check-label"  for="${item.id}" style="font-size: 16px; font-family: segoe">` +
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

            // fill the question types in the sidebar
            questionTypeInfo.map(item => {
                $("#question-type-choices").append(
                    `<div class="form-check d-flex align-items-center my-2 p-0" style="direction: ltr">` +
                        `<input class="form-check-input question-type-item" type="checkbox" id="${item.name}" onclick="filtering()">` +
                        `<label class="form-check-label"  for="${item.name}" style="font-size: 17px">` +
                            `${item.value}` +
                        `</label>` +
                    `</div>`
                )
            });


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

            // console.log(examList);
            examList.map(item => {
                $("#show-exams-container").append(
                    `<div class="col-12 mb-0 ${item.category}-box">` +
                        `<b class="mr-2" style="font-size: 18px; font-family: segoe, Yekan; font-weight: bold">${item.category}</b>` +
                        `<hr class="mt-1 mb-0">` +
                        `<div class="book-carousel p-3" id="${item.category}">` +

                        `</div>` +
                    `</div>`
                );
                item.exams.map(itm => {
                    // console.log(item.category);
                    $(`#${item.category}`).append(
                        `<div class="view overlay zoom book-cart" id="exam-${itm.id}" style="overflow: hidden" book="${itm.book}">` +
                            `<img src="${itm.image}" class="img-fluid rounded exam-image" alt="${itm.name}" style="height: 200px!important; width: 100%">` +
                            `<div class="mask row m-0 flex-center take-test">` +
                                `<div class="col-12 d-flex justify-content-center align-items-center bg-light px-4" style="position: absolute; top: 10%; width: fit-content; border-radius: 15px">` +
                                    `<p class="text-center my-1" style="font-family: segoe">${itm.book.name}</p>` +
                                `</div>`+
                                `<div class="col-12 d-flex justify-content-center align-items-center bg-light px-4" style="position: absolute; top: 30%; width: fit-content; border-radius: 15px; padding-top: 3px; padding-bottom: 5px" id="exam-${itm.id}-categories">` +
                                    // Categories of This Exam will show here
                                `</div>`+
                                `<div class="col-12 d-flex" style="position: absolute; top: 55%">` +
                                    `<button class="btn peach-gradient w-100 z-depth-4 btn-rounded mx-3" style="font-family: segoe; font-weight: bold; color: black">Take Test</button>`+
                                `</div>` +
                            `</div>` +
                            `<p class="text-uppercase text-center mt-2 mb-0" style="font-family: segoe, Yekan; font-weight: bold">${itm.name}</p>` +
                        `</div>`
                    );
                    let examCategoryName = [];
                    itm.categories.map(category => {
                        examCategoryName.push(category.name);
                        // console.log(examCategoryName);
                        // console.log(category)

                    });
                    $(`#exam-${itm.id}-categories`).empty();
                    examCategoryName = examCategoryName.toString();
                    let examCatList = examCategoryName.split(',');
                    let finalExamCategories = examCatList.join(" - ");
                    // console.log(finalExamCategories);
                    $(`#exam-${itm.id}-categories`).append(
                        `<p class="text-center" style="font-family: segoe, Yekan">${finalExamCategories}</p>`
                    );
                    itm.question_type.map(type => {
                        $(`#exam-${itm.id}`).attr('questionType', type.name)
                    });
                    itm.categories.map(type => {
                        $(`#exam-${itm.id}`).attr('categories', type.id)
                    });
                })
            });
            addOwl()

            $(".book-page-loader").addClass('d-none').removeClass('d-flex');
        }

    })
}

function activeBtn() {
    var btnContainer = document.getElementById("exam-categories");
    var btns = btnContainer.getElementsByClassName("btn");
    for (var i = 0; i < btns.length; i++) {
        // console.log("btns: " + btns.length);
      btns[i].addEventListener("click", function(){
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
      });
    }
}

function addOwl() {
    $(".book-carousel").addClass('owl-carousel').addClass('owl-theme');
    // $(".book-cart").addClass('col-auto').addClass('col-md-6').addClass('col-lg-4').addClass('my-3');
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
                items:2
            },
            1000:{
                items:3
            }
        }
    });
}
let selectedTypes = [];
let selectedBooks = [];
let selectedCategories = [];
function filtering(){
    // console.log(QTypeId.id);
    selectedTypes = [];
    selectedBooks = [];
    selectedCategories = [];
    $(".question-type-item").each(function (index){
        if($(this).is(':checked')){
            selectedTypes.push($(this).attr('id'))
        }
    });
    $(".book-name-item").each(function () {
        if($(this).is(':checked')){
            selectedBooks.push($(this).attr('id'))
        }
    });
    if (selectedTypes.toString() === '' && selectedBooks.toString() === '') {
        $(`#show-exams-container`).empty();
        $("#exam-categories").empty();
        $("#exam-categories").append(
            `<button class="btn btn-sm btn-rounded active" style="font-size: 12px" onclick="filterSelection('all')"> Show all</button>`
        );
        $("#question-type-choices").empty();
        $("#passage-type-choices").empty();
        $("#cambridge-book-choices").empty();
        getData()
    } else {
        $(".book-page-loader").removeClass('d-none').addClass('d-flex');
        $.ajax({
        url: 'http://127.0.0.1:8000/api/book/',
        type: "GET",
        dataType: 'json',
        data: {
            'question_type': selectedTypes.toString(),
            'book': selectedBooks.toString()
        },
        success: function (data) {
            let examInfo = [];
            // console.log(JSON.stringify(data));
            data["exams"].map(item => {
                examInfo.push({
                    id: item["id"],
                    book: item["book"]["name"],
                    name: item["name"],
                    image: item["image"],
                    categories: item["categories"],
                    questionTypes: item["questions_type"]
                })
            });
            $(`#show-exams-container`).empty();
            examInfo.map(itm => {
                // console.log(itm);
                // $(`#show-exams-container`).addClass('bg-danger');
                $(`#show-exams-container`).append(
                    `<div class="col-12 view col-md-6 col-lg-4 overlay zoom book-cart my-4" id="exam-${itm.id}" style="overflow: hidden" book="${itm.book}">` +
                        `<img src="${itm.image}" class="img-fluid rounded exam-image" alt="${itm.name}" style="height: 200px!important; width: 100%">` +
                        `<div class="mask row m-0 flex-center take-test">` +
                            `<div class="col-12 d-flex justify-content-center align-items-center bg-light px-4" style="position: absolute; top: 10%; width: fit-content; border-radius: 15px">` +
                                `<p class="text-center my-1" style="font-family: segoe">${itm.book}</p>` +
                            `</div>`+
                            `<div class="col-12 d-flex justify-content-center align-items-center bg-light px-4" style="position: absolute; top: 30%; width: fit-content; border-radius: 15px; padding-top: 3px; padding-bottom: 5px" id="exam-${itm.id}-categories">` +
                                // Categories of This Exam will show here
                            `</div>`+
                            `<div class="col-12 d-flex" style="position: absolute; top: 55%">` +
                                `<button class="btn peach-gradient w-100 z-depth-4 btn-rounded mx-3" style="font-family: segoe; font-weight: bold; color: black">Take Test</button>`+
                            `</div>` +
                        `</div>` +
                        `<p class="text-uppercase text-center mt-2 mb-0" style="font-family: segoe, Yekan; font-weight: bold">${itm.name}</p>` +
                    `</div>`
                );
                let examCategoryName = [];
                itm.categories.map(category => {
                    examCategoryName.push(category.name);
                    // console.log(examCategoryName);
                    // console.log(category)

                });
                examCategoryName = examCategoryName.toString();
                let examCatList = examCategoryName.split(',');
                let finalExamCategories = examCatList.join(" - ");
                // console.log(examCategoryName);
                $(`#exam-${itm.id}-categories`).append(
                    `<p class="text-center" style="font-family: segoe, Yekan">${finalExamCategories}</p>`
                )
            })
            // console.log(examInfo.categories)
            $(".book-page-loader").addClass('d-none').removeClass('d-flex');
        }
    })
    }



}