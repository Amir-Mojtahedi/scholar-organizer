const submit = document.querySelector("button[type=submit]")
const container = document.querySelector("#group-container")
const overlay = document.querySelector(".overlay")

//edit
document.querySelectorAll("button.orange").forEach(button => button.addEventListener("click", () => {
    openForm(1, button.getAttribute("data-group-id"), button.getAttribute("data-group-name"))
}))

//delete is a bit special because it doesn't need a form
document.querySelectorAll("button.red").forEach(button => button.addEventListener("click", () => {
    button.setAttribute("aria-busy", "true")
    openForm(2, button.getAttribute("data-group-id"), button.getAttribute("data-group-name"))
}))

//reuse this function for 3 different forms
const openForm = (actionId, groupId, groupName) => {
    if (actionId === 1) { //edit
        submit.innerText = "Edit Group"

        //manually changing form data for simplicity
        container.querySelector("form").action = `/groups/edit/`
        container.querySelector("input[name=id]").value = groupId
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        container.querySelector("form").action = `/groups/delete/`
        container.querySelector("input[name=name]").value = groupName
        container.querySelector("input[name=id]").value = groupId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    container.style.display = "flex"
    overlay.classList.add("active")
}

document.addEventListener("submit", () => {
    submit.setAttribute("aria-busy", "true")
})