function countOrder(){
    const cartCounter=document.getElementById("cartCounter");
    let catchCount=parseInt(localStorage.getItem('count'));
    
    if(catchCount){
        catchCount++;
        localStorage.setItem('count',catchCount);
        cartCounter.textContent=catchCount;

    }else{
        localStorage.setItem('count',1);
        cartCounter.textContent=1;
    }
    

}

function nextPreOrder(){
    countOrder();
    // oderProduct();

}

function addCart(cart){
    cart.forEach((item,index)=>{
        item.addEventListener('click',()=>{
            nextPreOrder()
        })
    })
}

function restore(){
    let restoreLocalValue = parseInt(localStorage.getItem('count'));
    const cartCounter=document.getElementById("cartCounter");
    if(restoreLocalValue){
        cartCounter.textContent=restoreLocalValue;
    }

}


// function orderProduct(){

// }

function manageOrder(){
    const cart=document.querySelectorAll(".add-cart");
    restore();
    addCart(cart);

}


window.addEventListener("load",()=>{
    manageOrder();
});