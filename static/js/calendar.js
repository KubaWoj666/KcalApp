const addMealButtons = document.querySelectorAll("#add-meal-btn");
const mealDateInput = document.getElementById("id_meal_date");
const snackDateInput = document.getElementById("id_snack_date");

let selectedDate = null;

addMealButtons.forEach(button => {
    button.addEventListener("click", function () {
        selectedDate = this.getAttribute("data-date");
        if (!selectedDate) return;

        let [year, month, day] = selectedDate.split("-");
        month = month.padStart(2, "0");
        day = day.padStart(2, "0");
        const formattedDate = `${year}-${month}-${day}`;

        if (mealDateInput) mealDateInput.value = formattedDate;
        if (snackDateInput) snackDateInput.value = formattedDate;

        console.log("Ustawiona data:", formattedDate);
    });
});

const addMealForm = document.getElementById("add-meal-form")
const csrf = addMealForm.querySelector("[name='csrfmiddlewaretoken']");
const meal = document.getElementById("id_meal")
const portionIn = document.getElementById("id_portions")



addMealForm.addEventListener("submit", function (e){ 
    e.preventDefault()
    $('#mealModal').modal('hide');
    const fd = new FormData()

    fd.append("csrfmiddlewaretoken", csrf.value);
    fd.append("meal", meal.value)
    fd.append("date", selectedDate)
    fd.append("portions", portionIn.value)

    $.ajax({
        type: "POST",
        url: "/cal/cal/",
        data: fd,

        success: function(response){
            console.log(response)
            if (response.message){
                alert(response.message)
            }
            window.location.reload("Refresh")
        },

        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})


document.addEventListener("DOMContentLoaded", function () {
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(cookie => {
                let [name, value] = cookie.trim().split("=");
                if (name === "csrftoken") {
                    cookieValue = value;
                }
            });
        }
        return cookieValue;
    }

    document.querySelectorAll(".delete-meal-form").forEach((form) => {
        // form.querySelector("[name='csrfmiddlewaretoken']").value = getCSRFToken();

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            fetch(this.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    this.parentElement.remove();  // Usuwa <li> po usunięciu posiłku
                    location.reload("Refresh")

                }
            })
            .catch((error) => console.error("Error:", error));
        });
    });

    document.querySelectorAll(".delete-snack-form").forEach((form) => {
        // form.querySelector("[name='csrfmiddlewaretoken']").value = getCSRFToken();

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            fetch(this.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    this.parentElement.remove();  // Usuwa <li> po usunięciu posiłku
                    location.reload("Refresh")

                }
            })
            .catch((error) => console.error("Error:", error));
        });
    });
});
