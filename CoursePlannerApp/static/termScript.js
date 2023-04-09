    //Initializing global elements needed
    let termList = document.getElementsByName('termList')[0];
    let unorderedListItem = document.createElement('ul');
    let addTermBtn = document.getElementsByName("addTerm")[0];
    let url = "/api/terms/";
    let flashMsg = document.getElementsByClassName("flashMessages")[0];

    //Adding listener to btn
    addTermBtn.addEventListener('click', addTerm);


    //Appending ul to Competency Section
    termList.appendChild(unorderedListItem);

    //Fetch all competencies
    fetchAllTerms();


function fetchAllTerms(){
    //Fetch * competencies
    fetch(url).then((res) => { if(res.status==200){
                                                    return res.json();
                                }})
                                .then((data) => { 
                                    data.forEach(term => {
                                        let termItem = document.createElement('div')
                                        let termName = document.createElement('h3')
                                        termName.innerHTML = ` ${term['name']}`
                                        let termId = document.createElement('p')
                                        termId.innerHTML = ` Id: ${term['id']}`
                                        let editPicture = document.createElement('img')
                                        editPicture.setAttribute('src', '/static/edit.png')
                                        editPicture.setAttribute('class', 'editBtn')                                       
                                        let deletePicture = document.createElement('img')
                                        deletePicture.setAttribute('src', '/static/delete.png')
                                        deletePicture.setAttribute('class', 'deleteBtn')
                                        unorderedListItem.appendChild(termItem)
                                        termItem.appendChild(termName)
                                        termName.appendChild(editPicture)
                                        termName.appendChild(deletePicture)
                                        termItem.appendChild(termId)
                                    });
                                });
}                                                                

function addTerm(){
}
 


