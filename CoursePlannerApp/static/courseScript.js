    //Initializing global elements needed
    let courseList = document.getElementsByName('courseList')[0];
    let unorderedListItem = document.createElement('ul');
    let addCourseBtn = document.getElementsByName("addCourse")[0];
    let url = "/api/courses/";
    let flashMsg = document.getElementsByClassName("flashMessages")[0];

    //Adding listener to btn
    addCourseBtn.addEventListener('click', addCourse);


    //Appending ul to Competency Section
    courseList.appendChild(unorderedListItem);

    //Fetch all competencies
    fetchAllCourses();


function fetchAllCourses(){
    //Fetch * competencies
    fetch(url).then((res) => { if(res.status==200){
                                                    return res.json();
                                }})
                                .then((data) => { 
                                    data.forEach(course => {
                                        let courseItem = document.createElement('div')
                                        let courseName = document.createElement('h3')
                                        courseName.innerHTML = ` ${course['name']}`
                                        let courseId = document.createElement('p')
                                        courseId.innerHTML = ` Code: ${course['id']}`
                                        let courseDescription = document.createElement('p')
                                        courseDescription.innerHTML = ` Description: ${course['description']}`
                                        let courseTheoryHours = document.createElement('p')
                                        courseTheoryHours.innerHTML = ` Theory hours: ${course['theory_hours']}`
                                        let courseLabHours = document.createElement('p')
                                        courseLabHours.innerHTML = ` Lab hours: ${course['lab_hours']}`
                                        let courseWorkHours = document.createElement('p')
                                        courseWorkHours.innerHTML = ` Work hours: ${course['work_hours']}`                                        
                                        let editPicture = document.createElement('img')
                                        editPicture.setAttribute('src', '/static/edit.png')
                                        editPicture.setAttribute('class', 'editBtn')                                       
                                        let deletePicture = document.createElement('img')
                                        deletePicture.setAttribute('src', '/static/delete.png')
                                        deletePicture.setAttribute('class', 'deleteBtn')
                                        unorderedListItem.appendChild(courseItem)
                                        courseItem.appendChild(courseName)
                                        courseName.appendChild(editPicture)
                                        courseName.appendChild(deletePicture)
                                        courseItem.appendChild(courseId)
                                        courseItem.appendChild(courseDescription)
                                        courseItem.appendChild(courseTheoryHours)
                                        courseItem.appendChild(courseLabHours)
                                        courseItem.appendChild(courseWorkHours)
                                    });
                                });
}                                                                

function addCourse(){
}
 


