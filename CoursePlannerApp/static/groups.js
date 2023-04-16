const submit = document.querySelector("button[type=submit]")
const container = document.querySelector("#group-container")
const overlay = document.querySelector(".overlay")

const openForm = (actionId, groupId) => {
    submit.setAttribute("aria-busy", "false")

    if (actionId === 1) { //edit
        submit.innerText = "Edit Group"
        container.querySelector("form").action = `/groups/edit/`
        container.querySelector("input[name=id]").value = groupId
    }

    if (actionId === 2) { //delete
        submit.innerText = "Delete Group"
        container.querySelector("form").action = `/groups/delete/`
        container.querySelector("input[name=id]").value = groupId
    }

    container.style.display = "flex"
    overlay.classList.add("active")
}

document.addEventListener("submit", () => {
    submit.setAttribute("aria-busy", "true")
})