function openCategoryModal() {
    document.getElementById("categoryModal").style.display = "block";
}

function closeCategoryModal() {
    document.getElementById("categoryModal").style.display = "none";
}

function createCategory() {
    const categoryName = document.getElementById("newCategoryName").value;

    fetch("/category/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `name=${encodeURIComponent(categoryName)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            const categorySelect = document.getElementById("category");
            const newOption = document.createElement("option");
            newOption.value = data.id;
            newOption.textContent = data.name;
            categorySelect.appendChild(newOption);
            closeCategoryModal();
        }
    })
    .catch(error => console.error("Ошибка:", error));
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
