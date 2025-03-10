const recipesButtons = document.querySelectorAll(".recipe-btn")
const clickedButton = document.activeElement;
const recipeInfo = document.getElementById("recipe-info")
const recipeIngredients = document.getElementById("recipe-ingredients")
const selectedRecipeName = document.getElementById("selected-recipe-name")
const recipeTotals = document.getElementById("recipe-totals")
const portionInput = document.getElementById("portion-input")
const portionTotals = document.getElementById("portion-totals")
const mealForm = document.getElementById("meal-form")
const tablePortionTotalsWithExtraIngredient = document.getElementById("portion-totals-with-extra-ingredient")
const extraIngredientsList = document.getElementById("ingredient-list")


let recipeId = 0

// const actionValue = clickedButton;
 


recipesButtons.forEach(button => {
    button.addEventListener("click", function (e) {
        e.preventDefault()
        while(recipeIngredients.firstChild) recipeIngredients.removeChild(recipeIngredients.firstChild);
        while(recipeTotals.firstChild) recipeTotals.removeChild(recipeTotals.firstChild);
        while(portionTotals.firstChild) portionTotals.removeChild(portionTotals.firstChild);
        while(tablePortionTotalsWithExtraIngredient.firstChild) tablePortionTotalsWithExtraIngredient.removeChild(tablePortionTotalsWithExtraIngredient.firstChild);
        while(extraIngredientsList.firstChild) extraIngredientsList.removeChild(extraIngredientsList.firstChild);


        
        // recipeId = button.getAttribute("data-recipe-id")

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
                mealForm.style.display = ""
                

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
        console.log("OPA")
        portion = portionInput.value
        
        Object.entries(response.totals).forEach(([key, value]) => {
            td = document.createElement("td")
            portionTotals.appendChild(td)
            td.id = "portion-table-data"
            td.textContent = (value/portion).toFixed(2)            
        });

        const liExtra = document.getElementById("li-extra-ingredient")
        console.log(liExtra)
    })
}




// Pobieranie elementów
const extraIngredientSelect = document.getElementById("extra-ingredient");
const extraGramsInput = document.getElementById("extra-grams");
const addExtraButton = document.getElementById("add-extra");
const ingredientList = document.getElementById("ingredient-list");
const tableTotalsWithExtra = document.getElementById("portion-totals-with-extra-ingredient")

// Obsługa kliknięcia "Add"
addExtraButton.addEventListener("click", function () {
    // Pobranie wybranego produktu
    const selectedOption = extraIngredientSelect.options[extraIngredientSelect.selectedIndex];

    if (document.getElementById("li-extra-ingredient")) {
        alert("❌ Możesz dodać tylko jeden dodatkowy składnik!");
        return;
    }
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
    li.id = "li-extra-ingredient"
    li.innerHTML = `<strong>${productName}</strong>: ${grams}g - ${kcal} kcal, ${protein}g protein, ${fat}g fat, ${carbs}g carbs <button id="extra-ingredient-delete-button"><i style="color: red;" class="fa-solid fa-x"></i></button>`;
    ingredientList.appendChild(li);


    const portionTableData = document.querySelectorAll("#portion-table-data")
    const values = [kcal, protein, fat, carbs]; // Tablica wartości

    portionTableData.forEach((element, index) => {
        if (index < values.length) { // Upewniamy się, że nie wychodzimy poza zakres
            td = document.createElement("td")
            td.id = "table-data-extras"
            tableTotalsWithExtra.appendChild(td)
            td.textContent = (parseFloat(element.textContent) + parseFloat(values[index])).toFixed(2);
        }
    });

});

document.addEventListener("click", function (e) {
    // Sprawdzamy, czy kliknięty element to przycisk usuwania
    if (e.target.closest("#extra-ingredient-delete-button")) {
        e.preventDefault();

        
        const liToRemove = e.target.closest("li"); // Pobieramy najbliższy element <li>
        
        if (liToRemove) {
            console.log("Usuwany składnik:", liToRemove.textContent);
            const liText = liToRemove.textContent; // Pobieramy tekst przed usunięciem
            liToRemove.remove(); // Usuwamy element z listy
            updateTableAfterRemoval(liText); // Przekazujemy usunięty tekst do funkcji
        }
    }
});

function updateTableAfterRemoval(liText) {
    const portionTableWithExtra = document.getElementById("portion-totals-with-extra-ingredient")
    while(portionTableWithExtra.firstChild) portionTableWithExtra.removeChild(portionTableWithExtra.firstChild);

    // const portionTableData = document.querySelectorAll("#table-data-extras");
//     console.log("Porcja przed aktualizacją:", portionTableData);


    

//     // Zerujemy wartości do odjęcia
//     let valuesToSubtract = [0, 0, 0, 0]; // kcal, protein, fat, carbs

//     // Wyszukujemy wartości do odjęcia na podstawie tekstu usuniętego składnika
//     const values = liText.match(/([\d\.]+) kcal, ([\d\.]+)g protein, ([\d\.]+)g fat, ([\d\.]+)g carbs/);
//     console.log("OPAAAA")
//     console.log(values)
//     if (values) {
//         console.log("Parsowane wartości:", values);

//         // Pobieramy wartości jako liczby i zapisujemy w tablicy
//         valuesToSubtract[0] = parseFloat(values[1]) || 0; // kcal
//         valuesToSubtract[1] = parseFloat(values[2]) || 0; // protein
//         valuesToSubtract[2] = parseFloat(values[3]) || 0; // fat
//         valuesToSubtract[3] = parseFloat(values[4]) || 0; // carbs
//     }

//     console.log("Odejmowane wartości:", valuesToSubtract);

//     // Aktualizacja wartości w tabeli
//     portionTableData.forEach((td, index) => {
//         console.log(td.textContent)
//         const currentValue = parseFloat(td.textContent) || 0;
//         console.log(currentValue)
//         td.textContent = (currentValue - valuesToSubtract[index]).toFixed(2);
//         console.log(td.textContent)
//     });

//     console.log("Tabela po aktualizacji:", portionTableData);
}



const saveMealBtn = document.getElementById("save-meal")
csrf = mealForm.querySelector("[name='csrfmiddlewaretoken']")


console.log(recipeId)

mealForm.addEventListener("submit", function (e) {
    e.preventDefault()
    const numOfPortions = document.getElementById("portion-input")
    console.log(numOfPortions.value)
    const mealName = document.getElementById("selected-recipe-name")
    const tableDataWithExtra = document.querySelectorAll("#table-data-extras")
    const portionTable = document.querySelectorAll("#portion-table-data")

    console.log("OPA", recipeId)
    // let nutrition = []

    // tableDataWithExtra.forEach(element => {
    //     nutrition.push(element.textContent)
        
    // });

    // console.log(nutrition)

    
    // portionTable.forEach(element => {
    //     nutrition.push(element.textContent)
    // })
    

    // console.log(nutrition)
    const fd = new FormData()

    fd.append("recipe_id", recipeId);
    fd.append("num_of_portions", numOfPortions.value);
    fd.append("csrfmiddlewaretoken", csrf.value);
    fd.append("meal_name", mealName.textContent )

    tableDataWithExtra.forEach(element => {
        fd.append("nutrition[]", element.textContent)
        
    });

    if (tableDataWithExtra.length === 0){
        portionTable.forEach(element => {
            fd.append("nutrition[]", element.textContent)
            
        });
    }


    $.ajax({
        type: "POST",
        url: "/save-meal/",
        data: fd,
        processData: false,  
        contentType: false,

        success: function(response){
            if (response.success ){
                alert(response.message)
            }else{
                alert(response.error)
            }
            
        },

        error: function(response){
            console.log("ERROR")
        }

        
    })
    

})

