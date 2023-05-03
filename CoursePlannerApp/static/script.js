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

const searchables = document.querySelectorAll(".searchable")
const filter = document.querySelector("input[name=filter]")

filter.addEventListener("input", () => {
    searchables.forEach(searchable => {
        if (searchable.innerHTML.toLowerCase().includes(filter.value.toLowerCase())) searchable.style.display = "block"
        else searchable.style.display = "none"
    })
})