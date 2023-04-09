    //Initializing global elements needed
    let competencyList = document.getElementsByName('competencyList')[0];
    let unorderedListItem = document.createElement('ul');
    let addCompetencyBtn = document.getElementsByName("addCompetency")[0];
    let url = "/api/competencies/";
    let flashMsg = document.getElementsByClassName("flashMessages")[0];

    //Adding listener to btn
    addCompetencyBtn.addEventListener('click', addCompetency);


    //Appending ul to Competency Section
    competencyList.appendChild(unorderedListItem);

    //Fetch all competencies
    fetchAllCompetencies();


function fetchAllCompetencies(){
    //Fetch * competencies
    fetch(url).then((res) => { if(res.status==200){
                                                    return res.json();
                                }})
                                .then((data) => { 
                                    console.log(data)
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
                                        unorderedListItem.appendChild(competencyItem)
                                        competencyItem.appendChild(competencyName)
                                        competencyItem.appendChild(competencyId)
                                        competencyItem.appendChild(competencyAchievement)
                                        competencyItem.appendChild(competencyType)
                                    });
                                });
}                                                                

function addCompetency(){
}
 


