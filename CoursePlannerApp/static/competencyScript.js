    //Initializing global elements needed
    let competencyList = document.getElementsByName('competencyList')[0];
    let unorderedListItem = document.createElement('ul');
    let addCompetencyBtn = document.getElementsByName("addCompetency")[0];
    let url = "/api/competencies/";
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
                                    data.forEach(competency => {
                                        let competencyItem = document.createElement('div')
                                        let competencyName = document.createElement('h3')
                                        competencyName.innerHTML = ` ${competency['name']}`
                                        let competencyId = document.createElement('p')
                                        competencyId.innerHTML = ` Code: ${competency['id']}`
                                        let competencyAchievement = document.createElement('p')
                                        competencyAchievement.innerHTML = ` Achievment: ${competency['achievement']}`
                                        let competencyType = document.createElement('p')
                                        competencyType.innerHTML = ` Type: ${competency['type']}`
                                        let editPicture = document.createElement('img')
                                        editPicture.setAttribute('src', '/static/edit.png')
                                        editPicture.setAttribute('class', 'editBtn')                                       
                                        let deletePicture = document.createElement('img')
                                        deletePicture.setAttribute('src', '/static/delete.png')
                                        deletePicture.setAttribute('class', 'deleteBtn')
                                        unorderedListItem.appendChild(competencyItem)
                                        competencyItem.appendChild(competencyName)
                                        competencyName.appendChild(editPicture)
                                        competencyName.appendChild(deletePicture)
                                        competencyItem.appendChild(competencyId)
                                        competencyItem.appendChild(competencyAchievement)
                                        competencyItem.appendChild(competencyType)
                                    });
                                });
}                                                                

function addTerm(){
}
 


