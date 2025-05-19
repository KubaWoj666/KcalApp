// DOM Elements
const recipesButtons = document.querySelectorAll(".recipe-btn");
const recipeInfo = document.getElementById("recipe-info");
const recipeIngredients = document.getElementById("recipe-ingredients");
const selectedRecipeName = document.getElementById("selected-recipe-name");
const recipeTotals = document.getElementById("recipe-totals");
const portionInput = document.getElementById("portion-input");
const portionTotals = document.getElementById("portion-totals");
const mealForm = document.getElementById("meal-form");
const tablePortionTotalsWithExtraIngredient = document.getElementById("portion-totals-with-extra-ingredient");
const extraIngredientsList = document.getElementById("ingredient-list");

let recipeId = 0;

recipesButtons.forEach(button => {
    button.addEventListener("click", function (e) {
        e.preventDefault();
        [recipeIngredients, recipeTotals, portionTotals, tablePortionTotalsWithExtraIngredient, extraIngredientsList].forEach(el => el.innerHTML = "");

        portionInput.value = 0;
        recipeId = e.target.getAttribute("data-recipe-id");

        $.ajax({
            type: "GET",
            url: `/get-recipe/${recipeId}`,
            success: function(response) {
                selectedRecipeName.textContent = response.name;
                recipeInfo.style.display = "";
                mealForm.style.display = "";

                response.ingredients.forEach(product => {
                    const li = document.createElement('li');
                    li.textContent = `${product.product}: ${product.grams}g`;
                    recipeIngredients.appendChild(li);
                });

                Object.entries(response.totals).forEach(([key, value]) => {
                    const td = document.createElement("td");
                    td.textContent = value;
                    recipeTotals.appendChild(td);
                });

                calculatePortion(response);
            }
        });
    });
});

function calculatePortion(response) {
    const infinitePortions = document.getElementById("infinite-portions-checkbox");

    infinitePortions.addEventListener("change", function () {
        portionTotals.innerHTML = "";
        if (infinitePortions.checked) portionInput.value = 0;

        Object.entries(response.totals).forEach(([key, value]) => {
            const td = document.createElement("td");
            td.id = "portion-table-data";
            td.textContent = (value / 1).toFixed(2);
            portionTotals.appendChild(td);
        });
        updateTotalsWithExtras();
    });

    portionInput.addEventListener("input", function () {
        portionTotals.innerHTML = "";
        infinitePortions.checked = false;

        let portion = parseFloat(portionInput.value);
        if (!portion || portion <= 0) portion = 1;

        Object.entries(response.totals).forEach(([key, value]) => {
            const td = document.createElement("td");
            td.id = "portion-table-data";
            td.textContent = (value / portion).toFixed(2);
            portionTotals.appendChild(td);
        });
        updateTotalsWithExtras();
    });
}

// Extra Ingredients Logic
const extraIngredientSelect = document.getElementById("extra-ingredient");
const extraGramsInput = document.getElementById("extra-grams");
const addExtraButton = document.getElementById("add-extra");

addExtraButton.addEventListener("click", function () {
    const selectedOption = extraIngredientSelect.options[extraIngredientSelect.selectedIndex];
    if (!selectedOption.value) return alert("Wybierz składnik!");

    const grams = parseFloat(extraGramsInput.value);
    if (isNaN(grams) || grams <= 0) return alert("Podaj poprawną ilość gramów!");

    const productName = selectedOption.textContent;
    const kcal = ((parseFloat(selectedOption.getAttribute("data-kcal")) / 100) * grams).toFixed(2);
    const protein = ((parseFloat(selectedOption.getAttribute("data-protein")) / 100) * grams).toFixed(2);
    const fat = ((parseFloat(selectedOption.getAttribute("data-fat")) / 100) * grams).toFixed(2);
    const carbs = ((parseFloat(selectedOption.getAttribute("data-carbs")) / 100) * grams).toFixed(2);

    const li = document.createElement("li");
    li.classList.add("li-extra-ingredient");
    li.innerHTML = `<strong>${productName}</strong>: ${grams}g - ${kcal} kcal, ${protein}g protein, ${fat}g fat, ${carbs}g carbs <button class="extra-ingredient-delete-button"><i style="color: red;" class="fa-solid fa-x"></i></button>`;
    extraIngredientsList.appendChild(li);

    updateTotalsWithExtras();
});

document.addEventListener("click", function (e) {
    if (e.target.closest(".extra-ingredient-delete-button")) {
        e.preventDefault();
        const liToRemove = e.target.closest("li");
        if (liToRemove) {
            liToRemove.remove();
            updateTotalsWithExtras();
        }
    }
});

function updateTotalsWithExtras() {
    const baseValues = document.querySelectorAll("#portion-table-data");
    const extraList = document.querySelectorAll(".li-extra-ingredient");

    const totals = [0, 0, 0, 0]; // kcal, protein, fat, carbs
    extraList.forEach(li => {
        const match = li.textContent.match(/([\d\.]+) kcal, ([\d\.]+)g protein, ([\d\.]+)g fat, ([\d\.]+)g carbs/);
        if (match) {
            totals[0] += parseFloat(match[1]);
            totals[1] += parseFloat(match[2]);
            totals[2] += parseFloat(match[3]);
            totals[3] += parseFloat(match[4]);
        }
    });

    tablePortionTotalsWithExtraIngredient.innerHTML = "";
    baseValues.forEach((cell, i) => {
        const td = document.createElement("td");
        td.id = "table-data-extras";
        td.textContent = (parseFloat(cell.textContent) + totals[i]).toFixed(2);
        tablePortionTotalsWithExtraIngredient.appendChild(td);
    });
}

// Form submission
const saveMealBtn = document.getElementById("save-meal");
const csrf = mealForm.querySelector("[name='csrfmiddlewaretoken']");

mealForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const numOfPortions = document.getElementById("portion-input");
    const infinitePortions = document.getElementById("infinite-portions-checkbox");
    const mealName = document.getElementById("selected-recipe-name");
    const tableDataWithExtra = document.querySelectorAll("#table-data-extras");
    const portionTable = document.querySelectorAll("#portion-table-data");

    const fd = new FormData();
    fd.append("recipe_id", recipeId);
    fd.append("infinite_portions", infinitePortions.checked);
    fd.append("num_of_portions", numOfPortions.value);
    fd.append("csrfmiddlewaretoken", csrf.value);
    fd.append("meal_name", mealName.textContent);

    const source = tableDataWithExtra.length > 0 ? tableDataWithExtra : portionTable;
    source.forEach(el => fd.append("nutrition[]", el.textContent));

    $.ajax({
        type: "POST",
        url: "/save-meal/",
        data: fd,
        processData: false,
        contentType: false,
        success: function(response) {
            alert(response.success ? response.message : response.error);
        },
        error: function(response) {
        }
    });
});
