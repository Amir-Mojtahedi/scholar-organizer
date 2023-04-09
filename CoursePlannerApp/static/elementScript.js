    //Initializing global elements needed
    let elementList = document.getElementsByName('elementList')[0];
    let unorderedListItem = document.createElement('ul');
    let addElementBtn = document.getElementsByName("addElement")[0];
    let url = "/api/elements/";
    let flashMsg = document.getElementsByClassName("flashMessages")[0];

    //Adding listener to btn
    addElementBtn.addEventListener('click', addElement);

    //Appending ul to Element Section
    elementList.appendChild(unorderedListItem);

    //Fetch all elements
    fetchAllElements();


function fetchAllElements(){
    //Fetch * elements
    fetch(url).then((res) => { if(res.status==200){
                                                    return res.json();
                                }})
                                .then((data) => { 
                                    data.forEach(element => {
                                        let elementItem = document.createElement('div')
                                        let elementName = document.createElement('h3')
                                        elementName.innerHTML = ` ${element['name']}`
                                        let elementOrder = document.createElement('p')
                                        let elementId = document.createElement('p')
                                        elementId.innerHTML = ` Id: ${element['id']}`
                                        elementOrder.innerHTML = ` Order: ${element['order']}`
                                        let elementCriteria = document.createElement('p')
                                        elementCriteria.innerHTML = ` Criteria: ${element['criteria']}`
                                        let elementCompetency = document.createElement('p')
                                        elementCompetency.innerHTML = ` Competency Id: ${element['competencyId']}`
                                        let editPicture = document.createElement('img')
                                        editPicture.setAttribute('src', '/static/edit.png')
                                        editPicture.setAttribute('class', 'editBtn')
                                        let deletePicture = document.createElement('img')
                                        deletePicture.setAttribute('src', '/static/delete.png')
                                        deletePicture.setAttribute('class', 'deleteBtn')
                                        unorderedListItem.appendChild(elementItem)
                                        elementItem.appendChild(elementName)
                                        elementName.appendChild(editPicture)
                                        elementName.appendChild(deletePicture)
                                        elementItem.appendChild(elementId)
                                        elementItem.appendChild(elementOrder)
                                        elementItem.appendChild(elementCriteria)
                                        elementItem.appendChild(elementCompetency)
                                        
                                    });
                                });
}                                                                

function addElement(){
}
 


