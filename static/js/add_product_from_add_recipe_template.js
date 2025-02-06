productForm = document.getElementById("create-product")
csrf = productForm.querySelector("[name='csrfmiddlewaretoken']")
const productList = document.getElementById("product_list")
    console.log(productList)
const url = "http://127.0.0.1:8000/create-product/"

document.getElementById('save_btn').addEventListener('click', function() {
    // Close Modal
    $('#exampleModal').modal('hide');
});

productForm.addEventListener("submit", function (e) {
    e.preventDefault()
    

    const form = e.target.closest("form")
    console.log(form)

    fd = new FormData(form)

    $.ajax({
        type: "POST",
        url:  "/create-product/",
        data: fd,
        dataType: "json",

        success: function (response) {
            updateProductDropdownList(response.new_product)
        },

        error: function (jqXHR, textStatus, errorThrown) {
            console.error("❌ Błąd:", textStatus);
            console.error("Szczegóły:", errorThrown);
        },
        cache: false,
        contentType: false,
        processData: false,
    })

})


function updateProductDropdownList(newProduct) {
    const select = document.getElementById("id_product")
    const productList = document.getElementById("product_list")
    console.log(productList)
   

    let optionExists = Array.from(select.options).some(option => option.value == newProduct.id)
    let itemExists = Array.from(productList.children).some(li => li.value == newProduct.name);

    if (!optionExists){
        const option = document.createElement("option")
        option.value = newProduct.id
        option.text = newProduct.name
        select.appendChild(option)
    }

    select.value = newProduct.id

    if (!itemExists){
        const li = document.createElement("li")
        li.textContent = `${newProduct.name} - ${newProduct.kcal} kcal/100g:`
        productList.appendChild(li)
    }
}