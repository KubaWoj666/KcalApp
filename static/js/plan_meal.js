const recipesButtons = document.querySelectorAll(".recipe-btn")
const clickedButton = document.activeElement;
const recipeInfo = document.getElementById("recipe-info")
const recipeIngredients = document.getElementById("recipe-ingredients")
const selectedRecipeName = document.getElementById("selected-recipe-name")
const recipeTotals = document.getElementById("recipe-totals")
const portionInput = document.getElementById("portion-input")
const portionTotals = document.getElementById("portion-totals")


// const actionValue = clickedButton;



recipesButtons.forEach(button => {
    button.addEventListener("click", function (e) {
        e.preventDefault()
        while(recipeIngredients.firstChild) recipeIngredients.removeChild(recipeIngredients.firstChild);
        while(recipeTotals.firstChild) recipeTotals.removeChild(recipeTotals.firstChild);
        while(portionTotals.firstChild) portionTotals.removeChild(portionTotals.firstChild);

        portionInput.value = 0
        const actionValue = e.target;
        recipeId = actionValue.getAttribute("data-recipe-id")
        
        $.ajax({
            type: "GET",
            url: `/get-recipe/${recipeId}`,
    
            success: function(response) {
                // console.log(response.totals)
                
    
                Object.entries(response.totals).forEach(([key, value]) => {
                    console.log(`${key}: ${value}`);
                });
    
                // recipe name
                selectedRecipeName.textContent = response.name
    
                // product list 
                recipeInfo.style.display = ""
                response.ingredients.forEach(product => {   
                    li = document.createElement('li')
                    recipeIngredients.appendChild(li)
                    li.textContent = product.product + ": " + product.grams+"g"
                });
                
                Object.entries(response.totals).forEach(([key, value]) => {
                    td = document.createElement("td")
                    recipeTotals.appendChild(td)
                    td.textContent = value
                    
                });

                calculatePortion(response)
                
    
            }
        })
    

    })
});


clickedButton.addEventListener("click", function (e) {

})



function calculatePortion(response){
    const portionInput = document.getElementById("portion-input")
    const portionTotals = document.getElementById("portion-totals")


    portionInput.addEventListener("change", function (e) {
        while(portionTotals.firstChild) portionTotals.removeChild(portionTotals.firstChild);

        portion = portionInput.value
        
        Object.entries(response.totals).forEach(([key, value]) => {
            td = document.createElement("td")
            portionTotals.appendChild(td)
            td.textContent = (value/portion).toFixed(2)
            
        });
    })
}



// const addExtraProductButton = document.getElementById("add-extra")
// const extraProduct = document.getElementById("extra-ingredient")

// extraProduct.addEventListener("change", function (e) {
//     const selectedOption = extraIngredientSelect.options[extraIngredientSelect.selectedIndex];

//     // Pobiera wartości atrybutów `data-*`
//     const productId = selectedOption.value;
//     const productName = selectedOption.textContent;
//     const kcal = selectedOption.getAttribute("data-kcal");
//     const protein = selectedOption.getAttribute("data-protein");
//     const fat = selectedOption.getAttribute("data-fat");
//     const carbs = selectedOption.getAttribute("data-carbs");

//     // Wyświetla dane w konsoli (możesz je wykorzystać w UI)
//     console.log(`Produkt: ${productName}`);
//     console.log(`ID: ${productId}`);
//     console.log(`Kalorie: ${kcal}`);
//     console.log(`Białko: ${protein}`);
//     console.log(`Tłuszcz: ${fat}`);
//     console.log(`Węglowodany: ${carbs}`);
// })


// Pobieranie elementów
const extraIngredientSelect = document.getElementById("extra-ingredient");
const extraGramsInput = document.getElementById("extra-grams");
const addExtraButton = document.getElementById("add-extra");
const ingredientList = document.getElementById("ingredient-list");

// Obsługa kliknięcia "Add"
addExtraButton.addEventListener("click", function () {
    // Pobranie wybranego produktu
    const selectedOption = extraIngredientSelect.options[extraIngredientSelect.selectedIndex];

    // Sprawdzenie, czy wybrano produkt
    if (!selectedOption.value) {
        alert("Wybierz składnik!");
        return;
    }

    // Pobranie wartości z inputa
    const grams = parseFloat(extraGramsInput.value);

    if (isNaN(grams) || grams <= 0) {
        alert("Podaj poprawną ilość gramów!");
        return;
    }

    // Pobranie wartości odżywczych
    const productName = selectedOption.textContent;
    const kcalPer100g = parseFloat(selectedOption.getAttribute("data-kcal"));
    const proteinPer100g = parseFloat(selectedOption.getAttribute("data-protein"));
    const fatPer100g = parseFloat(selectedOption.getAttribute("data-fat"));
    const carbsPer100g = parseFloat(selectedOption.getAttribute("data-carbs"));

    // Przeliczenie wartości na podaną ilość gramów
    const kcal = ((kcalPer100g / 100) * grams).toFixed(2);
    const protein = ((proteinPer100g / 100) * grams).toFixed(2);
    const fat = ((fatPer100g / 100) * grams).toFixed(2);
    const carbs = ((carbsPer100g / 100) * grams).toFixed(2);

    // Dodanie produktu do listy
    const li = document.createElement("li");
    li.innerHTML = `<strong>${productName}</strong>: ${grams}g - ${kcal} kcal, ${protein}g protein, ${fat}g fat, ${carbs}g carbs`;
    ingredientList.appendChild(li);
});
