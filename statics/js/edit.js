const saveButton = document.getElementById("save-btn");
const saveAsNewButton = document.getElementById("save-as-new-btn");
const editForm = document.getElementById("edit-form");

function saveObject(e) {
    e.preventDefault();
    editForm.save.value = "Save";
    editForm.submit();
}


function saveAsNewObject(e) {
    e.preventDefault();
    editForm.save.value = "Save as new";
    editForm.submit();
}


saveButton.addEventListener("click", saveObject)
saveAsNewButton.addEventListener("click", saveAsNewObject)
