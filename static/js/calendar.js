const addMealButton = document.querySelectorAll("#add-meal-btn");
const dateInput = document.getElementById("id_date")


let selectedDate = 0

addMealButton.forEach(element => {
    element.addEventListener("click", function (e) {
        selectedDate = this.getAttribute("data-date")
        console.log(selectedDate)

        
        
        if (dateInput){
            let [year, month, day] = selectedDate.split("-");
            month = month.padStart(2, "0");  // Dodaje zero, jeśli miesiąc ma tylko 1 cyfrę
            day = day.padStart(2, "0");  // Dodaje zero, jeśli dzień ma tylko 1 cyfrę

            selectedDate = `${year}-${month}-${day}`;
            dateInput.value = selectedDate;
            console.log("Ustawiona data:", dateInput.value);  // Sprawdzenie w konsoli

        }
    })
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
