const saveButton = document.getElementById("save-btn");
const saveAndAddAnotherButton = document.getElementById("save-and-add-another-btn");
const createForm = document.getElementById("create-form");

function saveObject(e) {
    e.preventDefault();
    createForm.save.value = "Save";
    createForm.submit();
}


function saveAndAddAnotherObject(e) {
    e.preventDefault();
    createForm.save.value = "Save and add another";
    createForm.submit();
}


saveButton.addEventListener("click", saveObject)
saveAndAddAnotherButton.addEventListener("click", saveAndAddAnotherObject)
