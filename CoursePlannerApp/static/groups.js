const container = document.querySelector(".container-fluid.overlay")
const form = container.querySelector("form")
const submit = form.querySelector("button[type=submit]")

//button actions
document.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    if (button.classList.contains("close")) return closeForm()
    else if (button.classList.contains("add")) return openForm(0, button) //pass in any element here... doesn't matter
    else if (button.classList.contains("edit")) return openForm(1, button.parentElement.parentElement)

    else if (button.classList.contains("delete")) openForm(2, button.parentElement.parentElement)
    else return

    button.setAttribute("aria-busy", "true")
}))

//close form gently and prep for reopening
const closeForm = () => {
    container.style.animation = "slideFadeOut 0.5s"

    setTimeout(() => {
        container.style.display = "none"
        container.classList.remove("active")
        container.style.animation = "slideFadeIn 0.5s"
    }, 500)

    //reset form data
    form.querySelector("input[name=name]").value = ""
}

//configures the multipurpose form and opens it
const openForm = (actionId, wrapper) => {
    const groupId = wrapper.getAttribute("data-group-id")
    const groupName = wrapper.getAttribute("data-group-name")

    if (actionId === 0) { //add
        submit.innerText = "Add Group"

        //manually changing form data for simplicity
        form.action = "/groups/"
    }

    if (actionId === 1) { //edit
        submit.innerText = "Edit Group"

        //manually changing form data for simplicity
        form.action = "/groups/edit/"
        form.querySelector("input[name=id]").value = groupId
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        form.action = "/groups/delete/"
        form.querySelector("input[name=name]").value = groupName
        form.querySelector("input[name=id]").value = groupId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    container.style.display = "flex"
    container.classList.add("active")
}

document.addEventListener("submit", e => {
    e.preventDefault()

    console.log(form.checkValidity())

    //manually submit form
    if (form.checkValidity()) {
        form.submit()
        submit.setAttribute("aria-busy", "true")
    }
})