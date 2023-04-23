const container = document.querySelector(".container-fluid.overlay")
const form = container.querySelector("form")
const submit = form.querySelector("button[type=submit]")
const deleteBtn = document.getElementsName('delete')

//delete is a bit special because it doesn't need a form
deleteBtn.forEach(button => button.addEventListener("click", () => {
    button.setAttribute("aria-busy", "true")
    openForm(2, button.getAttribute("data-course-id"), button.getAttribute("data-course-name"), button.getAttribute("data-course-theoryHours"), button.getAttribute("data-course-labHours"), button.getAttribute("data-course-workHours"), button.getAttribute("data-course-description"), button.getAttribute("data-course-termId"), button.getAttribute("data-course-domainId"))
}))

//reuse this function for 3 different forms
const openForm = (actionId, courseId, courseName, courseTheory_hours, courseLab_hours, courseWork_hours, courseDescription, courseTermId, courseDomainId) => {
    if (actionId === 1) { //edit
        submit.innerText = "Edit Course"

        //manually changing form data for simplicity
        form.action = `/courses/edit/`
        form.querySelector("input[name=id]").value = courseId
    }

    if (actionId === 2) { //delete
        //manually changing form data for simplicity
        form.action = `/groups/delete/`
        form.querySelector("input[name=id]").value = courseId
        form.querySelector("input[name=name]").value = courseName
        form.querySelector("input[name=theory_hours]").value = courseTheory_hours
        form.querySelector("input[name=lab_hours]").value = courseLab_hours
        form.querySelector("input[name=work_hours]").value = courseWork_hours
        form.querySelector("input[name=description]").value = courseDescription
        form.querySelector("input[name=termId]").value = courseTermId
        form.querySelector("input[name=domainId]").value = courseDomainId

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