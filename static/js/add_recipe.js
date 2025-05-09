document.addEventListener("DOMContentLoaded", function () {
    const recipeForm = document.getElementById("recipe-form");
    if (!recipeForm) {
        console.error("❌ Nie znaleziono formularza recipeForm!");
        return;
    }

    const csrf = recipeForm.querySelector("[name='csrfmiddlewaretoken']");
    const recipeNameInput = document.getElementById("id_name");
    const productSelectInput = document.getElementById("id_product");
    const gramsInput = document.getElementById("id_grams");
    const selectedProductsList = document.getElementById("selected-products-list");

    const url = "/add-recipe/";

    recipeForm.addEventListener("submit", function (e) {
        e.preventDefault(); // ZATRZYMAJ PRZEŁADOWANIE STRONY

        const clickedButton = document.activeElement;
        const actionValue = clickedButton.value;

        const fd = new FormData();
        fd.append("csrfmiddlewaretoken", csrf.value);
        fd.append("name", recipeNameInput.value);
        fd.append("product", productSelectInput.value);
        fd.append("grams", gramsInput.value);
        fd.append("action", actionValue);

        $.ajax({
            type: "POST",
            url: url,
            data: fd,
            success: function (response) {
                const product = response.product;
                const grams = response.grams;

                if (product && grams) {
                    const listItem = document.createElement("li");
                    listItem.setAttribute("name", "selected-product");
                    listItem.setAttribute("id", "prod-list");
                    listItem.textContent = `${product} - ${grams}g`;

                    listItem.innerHTML += `
                        <form method="post" name="delete-form" action="/delete-from-product-list/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf.value}">
                            <input type="hidden" name="recipe-name" value="${recipeNameInput.value}">
                            <input type="hidden" name="product" value="${product}">
                            <input type="hidden" name="grams" value="${grams}">
                            <button name="action" type="submit" class="delete-button"><i class="fa-solid fa-x"></i></button>
                        </form>`;
                    selectedProductsList.appendChild(listItem);

                    gramsInput.value = "";
                } else {
                    alert("Wybierz produkt i podaj gramaturę.");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("❌ Błąd:", textStatus);
                console.error("Szczegóły:", errorThrown);
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });

    // 🛠 Obsługa usuwania produktu – działa na dynamicznie dodanych elementach
    document.getElementById("selected-products-list").addEventListener("click", function (e) {
        if (e.target && e.target.closest(".delete-button")) {
            e.preventDefault();

            const form = e.target.closest("form");
            if (!form) return;

            const fd = new FormData(form);

            $.ajax({
                type: "POST",
                url: "/delete-from-product-list/",
                data: fd,
                success: function (response) {
                    form.closest("li").remove();
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error("❌ Błąd:", textStatus);
                    console.error("Szczegóły:", errorThrown);
                },
                cache: false,
                contentType: false,
                processData: false,
            });
        }
    });
});
