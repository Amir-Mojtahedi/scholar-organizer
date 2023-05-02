const form = document.querySelector("form")
const submit = document.querySelector("button[type=submit]")

document.addEventListener("submit", e => {
    e.preventDefault()

    //manually submit form
    if (form.checkValidity()) {
        submit.setAttribute("aria-busy", "true")

        form.submit()
    }
})