const container = document.querySelector(".container-fluid.overlay")
const form = container.querySelector("form")
const submit = form.querySelector("button[type=submit]")

//button actions
document.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    if (button.classList.contains("close")) return closeForm()
    if (button.classList.contains("add")) return openForm(0, button.parentElement)
    if (button.classList.contains("edit")) return openForm(1, button.parentElement.parentElement)

    if (button.classList.contains("delete")) openForm(2, button.parentElement.parentElement)
    if (button.classList.contains("block")) openForm(3, button.parentElement.parentElement)
    if (button.classList.contains("unblock")) openForm(4, button.parentElement.parentElement)
    button.setAttribute("aria-busy", "true")
}))

document.querySelector("details").addEventListener("click", () => {
    if (form.querySelector("details").open) {
        const selected = form.querySelector("details").querySelector("input:checked")
        form.querySelector("summary").innerText = selected.parentElement.innerText
    }
})

//close gently and prep for reopening
const closeForm = () => {
    container.style.animation = "slideFadeOut 0.5s"

    setTimeout(() => {
        container.style.display = "none"
        container.classList.remove("active")
        container.style.animation = "slideFadeIn 0.5s"

        //hide group selection
        form.querySelector("details").hidden = true
    }, 500)
}

//reuse this function for 3 different forms
const openForm = (actionId, wrapper) => {
    const userId = wrapper.getAttribute("data-user-id")
    const userName = wrapper.getAttribute("data-user-name")
    const groupId = wrapper.getAttribute("data-group-id")
    const groupName = wrapper.getAttribute("data-group-name")

    submit.innerHTML = "Add User to <mark>" + groupName + "</mark>"

    if (actionId === 1) { //edit
        submit.innerText = "Edit User"
        form.querySelector("summary").innerText = groupName

        //show group selection
        form.querySelector("details").hidden = false
        form.querySelector("details").querySelector(`input[value="${groupId}"]`).checked = true

        //manually changing form data for simplicity
        form.action = `/users/edit/`
        form.querySelector("input[name=id]").value = userId
        form.querySelector("input[name=group_id]").value = form.querySelector("details").querySelector("input:checked").value
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        form.action = `/users/delete/`
        form.querySelector("input[name=id]").value = userId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    if (actionId === 3) { //block
        //manually changing form data for simplicity
        form.action = `/users/block/`
        form.querySelector("input[name=id]").value = userId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    if (actionId === 4) { //unblock
        //manually changing form data for simplicity
        form.action = `/users/unblock/`
        form.querySelector("input[name=id]").value = userId

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