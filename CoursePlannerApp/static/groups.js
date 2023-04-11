const editGroup = async id => {
    const name = prompt("Edit group", "Enter a new name for this group!")
    if (name.length === 0) return alert("The group name cannot be empty!")

    const req = await fetch(`/groups/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ id: id, name: name }),
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (req.status === 200) alert("The group has successfully been edited!")
    else {
        const res = await req.json()
        alert(res.error)
    }
}

const deleteGroup = async id => {
    if (!confirm("Are you sure you want to delete this group?")) return

    if ([0, 1, 2].includes(+id)) return alert("You cannot delete this group!")

    const req = await fetch(`/groups/${id}`, {
        method: "DELETE"
    })

    if (req.status === 200) alert("The group has successfully been deleted!")
    else {
        const res = await req.json()
        alert(res.error)
    }
}