const container = document.querySelector(".container-fluid.overlay")
const form = container.querySelector("form")
const submit = form.querySelector("button[type=submit]")

//edit
document.querySelectorAll(".buttons button.orange").forEach(button => button.addEventListener("click", () => {
    openForm(1, button.getAttribute("data-user-id"), button.getAttribute("data-user-name"), button.getAttribute("data-group-id"), button.getAttribute("data-group-name"))
}))

//delete is a bit special because it doesn't need a form
document.querySelectorAll(".buttons button.red").forEach(button => button.addEventListener("click", () => {
    button.setAttribute("aria-busy", "true")
    openForm(2, button.getAttribute("data-user-id"), button.getAttribute("data-user-name"), button.getAttribute("data-group-id"), button.getAttribute("data-group-name"))
}))

//close form
container.querySelector("button.close").addEventListener("click", () => {
    container.style.animation = "slideFadeOut 0.5s"
    setTimeout(() => {
        container.style.display = "none"
        container.classList.remove("active")
        container.style.animation = "slideFadeIn 0.5s"
    }, 500)
})

//reuse this function for 3 different forms
const openForm = (actionId, userId, userName, groupId, groupName) => {
    if (actionId === 1) { //edit
        submit.innerText = "Edit User"
        form.querySelector("summary").innerText = groupName

        //manually changing form data for simplicity
        form.action = `/users/edit/`
        form.querySelector("input[name=id]").value = userId
        form.querySelector("input[name=group_id]").value = groupId
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        form.action = `/users/delete/`
        form.querySelector("input[name=name]").value = groupName
        form.querySelector("input[name=id]").value = groupId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    container.style.display = "flex"
    container.classList.add("active")
}

document.addEventListener("submit", () => {
    submit.setAttribute("aria-busy", "true")
})