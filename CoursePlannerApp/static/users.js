const container = document.querySelector(".container-fluid.overlay")
// const form = container.querySelector("form")
// const submit = form.querySelector("button[type=submit]")

//button actions
document.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
    if (button.classList.contains("close")) return closeForm()
    else if (button.classList.contains("add")) return openForm(0, button.parentElement)
    else if (button.classList.contains("edit")) return openForm(1, button.parentElement.parentElement)

    else if (button.classList.contains("delete")) {
        if (button.classList.contains("outline")) openForm(2, button.parentElement.parentElement)
        else {
            button.classList.add("outline")
            button.innerText = "Confirm"

            //change back after 3s
            setTimeout(() => {
                button.classList.remove("outline")
                button.innerText = "Delete"
            }, 3000)

            return
        }
    }
    else if (button.classList.contains("block")) openForm(3, button.parentElement.parentElement)
    else if (button.classList.contains("unblock")) openForm(4, button.parentElement.parentElement)
    else return

    button.setAttribute("aria-busy", "true")
}))

//group selection (making a details element act like a select element)
document.querySelector("details").addEventListener("click", () => {
    if (form.querySelector("details").open) {
        const selected = form.querySelector("details").querySelector("input:checked")
        form.querySelector("summary").innerText = selected.parentElement.innerText
        form.querySelector("input[name=group_id]").value = form.querySelector("details").querySelector("input:checked").value
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

    //reset form data
    form.querySelector("input[name=name]").value = ""
    form.querySelector("input[name=email]").value = ""
    form.querySelector("input[name=password]").value = ""
    form.querySelector("input[name=avatar]").value = ""
}

//configures the multipurpose form and opens it
const openForm = (actionId, wrapper) => {
    const userId = wrapper.getAttribute("data-user-id")
    const userName = wrapper.getAttribute("data-user-name")
    const userEmail = wrapper.getAttribute("data-user-email")
    const groupId = wrapper.getAttribute("data-group-id")
    const groupName = wrapper.getAttribute("data-group-name")

    if (actionId === 0) { //add
        submit.innerHTML = `Add User to <mark>${groupName}</mark>`

        //manually changing form data for simplicity
        form.action = "/users/"
        form.querySelector("input[name=group_id]").value = groupId
    }

    if (actionId === 1) { //edit
        submit.innerText = "Edit User"
        form.querySelector("summary").innerText = groupName

        //show group selection
        form.querySelector("details").hidden = false
        form.querySelector("details").querySelector(`input[value="${groupId}"]`).checked = true

        //manually changing form data for simplicity
        form.action = "/users/edit/"
        form.querySelector("input[name=name]").value = userName
        form.querySelector("input[name=email]").value = userEmail
        form.querySelector("input[name=id]").value = userId
        form.querySelector("input[name=group_id]").value = groupId
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        form.action = "/users/delete/"
        form.querySelector("input[name=id]").value = userId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    if (actionId === 3) { //block
        //manually changing form data for simplicity
        form.action = "/users/block/"
        form.querySelector("input[name=id]").value = userId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    if (actionId === 4) { //unblock
        //manually changing form data for simplicity
        form.action = "/users/unblock/"
        form.querySelector("input[name=id]").value = userId

        //no need to actually show form, just submit
        document.querySelector("form").submit()
        return
    }

    container.style.display = "flex"
    container.classList.add("active")
}