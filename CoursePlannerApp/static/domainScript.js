    //Initializing global elements needed
    let domainList = document.getElementsByName('domainList')[0];
    let unorderedListItem = document.createElement('ul');
    let addDomainBtn = document.getElementsByName("addDomain")[0];
    let url = "/api/domains/";
    let flashMsg = document.getElementsByClassName("flashMessages")[0];

    //Adding listener to btn
    addDomainBtn.addEventListener('click', addDomain);


    //Appending ul to Competency Section
    domainList.appendChild(unorderedListItem);

    //Fetch all domains
    fetchAllDomains();


function fetchAllDomains(){
    //Fetch * domains
    fetch(url).then((res) => { if(res.status==200){
                                                    return res.json();
                                }})
                                .then((data) => { 
                                    data.forEach(domain => {
                                        let domainItem = document.createElement('div')
                                        let domainName = document.createElement('h3')
                                        domainName.innerHTML = ` ${domain['name']}`
                                        let domainId = document.createElement('p')
                                        domainId.innerHTML = ` Code: ${domain['id']}`
                                        let domainDescription = document.createElement('p')
                                        domainDescription.innerHTML = ` Description: ${domain['description']}`
                                        let editPicture = document.createElement('img')
                                        editPicture.setAttribute('src', '/static/edit.png')
                                        editPicture.setAttribute('class', 'editBtn')                                       
                                        let deletePicture = document.createElement('img')
                                        deletePicture.setAttribute('src', '/static/delete.png')
                                        deletePicture.setAttribute('class', 'deleteBtn')
                                        unorderedListItem.appendChild(domainItem)
                                        domainItem.appendChild(domainName)
                                        domainName.appendChild(editPicture)
                                        domainName.appendChild(deletePicture)
                                        domainItem.appendChild(domainId)
                                        domainItem.appendChild(domainDescription)
                                    });
                                });
}                                                                

function addDomain(){
}
 


