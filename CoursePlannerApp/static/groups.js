const submit = document.querySelector("button[type=submit]")

const openForm = () => {
    submit.setAttribute("aria-busy", "false")

    const container = document.querySelector("#group-container")
    container.style.display = "flex"

    const overlay = document.querySelector(".overlay")
    overlay.classList.add("active")
}

document.addEventListener("submit", () => {
    submit.setAttribute("aria-busy", "true")
})