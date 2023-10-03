console.log("working fine");
const monthName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
$("#commentForm").submit(function(e){
    e.preventDefault();
    let dt = new Date();
    let time = dt.getDay() + " " + monthName[dt.getUTCMonth()] + ", " + dt.getFullYear();
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("comment saved");
            if(response.bool == true){
                $("#review-res").html("Review Added")
                $(".hide-comment-form").hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html +='<div class="user justify-content-between d-flex">'
                    _html +='<div class="thumb text-center">'
                    _html +='<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html +='</div>'

                    _html +='<div class="desc">'
                    _html +='<div class="d-flex justify-content-between mb-10">'
                    _html +='<div class="d-flex align-items-center">'
                    _html +='<span class="font-xs text-muted">'+ time +' </span>'
                    _html +='</div>'
                    _html +='<div>'

                    _html +='</div>'

                    for(let i = 1; i <= response.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"> </i>'
                    }
                    _html +='</div>'
                    _html +='<p class="mb-10">'+ response.context.review +'</p>'
                    _html +='</div>'
                    _html +='</div>'
                    _html +='</div>'
                    $(".comment-list").prepend(_html)
            }
        }
    })
})


// Add to cart functionality
//$("#add-to-cart-btn").on("click",function(){
//    console.log("making add to cart");
//    let quantity = $("#product-quantity").val();
    //console.log(quantity);
//    let product_title = $(".product-title").val();
    //console.log(product_title);
//    let product_id = $(".product-id").val();
    //console.log(product_id);
//    let product_price = $("#current-product-price").text();
    //console.log(product_price);
//    let this_val = $(this);

//    $.ajax({
//        url: '/add-to-cart',
//        data: {
//            'id':product_id,
//            'qty': quantity,
//            'title': product_title,
//            'price': product_price,
//        },
//        dataType: 'json',
//        beforeSend: function(){
//            console.log("Adding product to cart");
//        },
//        success: function(response){
//            this_val.html("<i class='fas fa-check-circle'></i>")
//            console.log("added product to cart");
//            $(".cart-items-count").text(response.totalCartItems)
//        }
//    })
//})

$(".add-to-cart-btn").on("click",function(){
    let this_val = $(this)
    //console.log(this_val);
    let index_val = this_val.attr("data-index")
    //console.log(index_val);
    let quantity = $(".product-quantity-" + index_val).val();
    //console.log(quantity);
    let product_title = $(".product-title-" + index_val).val();
    //console.log(product_title);
    let product_id = $(".product-id-" + index_val).val();
    //console.log(product_id);
    let product_price = $(".current-product-price-" + index_val).text();
    //console.log(product_price);
    let product_pid = $(".product-pid-" + index_val).val();
    //console.log(product_pid);
    let product_image = $(".product-image-" + index_val).val();

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id':product_id,
            'pid':product_pid,
            'price':product_price,
            'quantity': quantity,
            'title': product_title,
            'img':product_image,
            'qty':quantity
        },
        dataType:'json',
        beforeSend:function(){
            console.log("Adding product to cart");
        },
        success: function(response){
            this_val.html("<i class='fas fa-check-circle'></i>")
            console.log("added product to cart");
            $(".cart-items-count").text(response.totalCartItems)
        }
    })
})