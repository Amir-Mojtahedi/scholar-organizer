INSERT INTO courseapp_groups(id, name) VALUES(0, 'Members');
INSERT INTO courseapp_groups(id, name) VALUES(1, 'Admin_user_gp');
INSERT INTO courseapp_groups(id, name) VALUES(2, 'Admin_gp');

INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(2, 'Instructor', 'instructor@dawsoncollege.qc.ca', 'pbkdf2:sha256:260000$YPhvHFnzU6CDfaWc$b48c6049b93a7b9e1dc5cfe44c48e589a202fc430cf31694dc85ac2f59d36493');

INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject1', 'testsubject1@dreamys.studio', 'pbkdf2:sha256:260000$gE0TgFCJYqgWLb6q$045358176cae301735a79f77fe92ef8452d2e74b0bb87fc6e5c65b15acbf4500');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject2', 'testsubject2@dreamys.studio', 'pbkdf2:sha256:260000$UjIFjAgiylZqgnBl$f1ab1aa9347bb891b92a261bfd453369f9dd11cd062dd8c78c16cc871797a470');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject3', 'testsubject3@dreamys.studio', 'pbkdf2:sha256:260000$8R5a5NvPNhN7mSmD$449e1d35c29f1a05ebce29f04e605a57d8e9210fff50e9bafee334d2bfb3b12a');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject4', 'testsubject4@dreamys.studio', 'pbkdf2:sha256:260000$sZuzzMAdEG57X69z$a56118142dde43229c512302d649a1e48365c050ef5806880be7ce72bbaf3ce6');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject5', 'testsubject5@dreamys.studio', 'pbkdf2:sha256:260000$0w6s1rOL2rygaUob$f36b97267020621a31b97ebf960c3075c06b3e2526d0dbd93509279d85fe27c1');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject6', 'testsubject6@dreamys.studio', 'pbkdf2:sha256:260000$5JEb7zGhgLBiafdv$7815f1eefb927b592f4393723c3d791f3a0b92942ad546b0a0417088b9c12307');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject7', 'testsubject7@dreamys.studio', 'pbkdf2:sha256:260000$1wAvP3j8bIzmBnhr$b30e6c83fea93235f28b92128f45514d8416cc5239fb4dfa65c9c883a48f1587');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject8', 'testsubject8@dreamys.studio', 'pbkdf2:sha256:260000$vWn637yq2Hde3K7G$e5db664b18353f2f250af1cfefc862a8aa9172e05fdca58a37744fc85024df38');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject9', 'testsubject9@dreamys.studio', 'pbkdf2:sha256:260000$5EH6z9QkyDhsBuvk$a59a0cfca9dafa00c78692c230661c48ee6d027a6f5013de4c9174d1f5797f10');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(0, 'Testsubject10', 'testsubject10@dreamys.studio', 'pbkdf2:sha256:260000$1XrgRvjVSg6vQOu8$5e90e43749512734ef942bda6815047ae0e1d109900d664e4e6ac3d00bab2fa7');

INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(1, 'Useradmin1', 'useradmin1@dreamys.studio', 'pbkdf2:sha256:260000$UGbCIjnQJ2OxZu1z$8fde08157d7400c5feef78f4017a5af64b12ab5cd3663ba0be854f85572293df');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(1, 'Useradmin2', 'useradmin2@dreamys.studio', 'pbkdf2:sha256:260000$CmvIHgRrOCe1r084$b1894de6186ad4b290e11b0e005aa7be70071043c93f1212f1a4f86f34eb73de');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(2, 'Admin1', 'admin1@dreamys.studio', 'pbkdf2:sha256:260000$D4ow6S4UUcLCHgpu$8fb6ea4e86eb54fff721929ea7cd86dc0062832f99f120ea0cb193d7953a285c');
INSERT INTO COURSEAPP_USERS(group_id, name, email, password) VALUES(2, 'Admin2', 'admin2@dreamys.studio', 'pbkdf2:sha256:260000$Q4UOkp2EQgWlYxOX$b66d2942edbe7d66c6810969445236647b5cd73b74609665e04997f21c695a7b');
--Sample Data
--base course
--PROGRAMMING I----------------------------------------------------------------------------------------------------------------------
    --Term
    insert into terms values (1, 'Fall');
    --Domain
    insert into domains values (1/*GENERATED*/, 'Programming, Data Structures, and Algorithms',
        --Description
        'The courses in the Programming, Data Structures and Algorithms domain teach the knowledge and skills required to design and program solutions to typical information technology problems. The students are taught object-oriented programming in the context of standalone, event-driven and web-based programs.');
    --Course
    insert into courses values ('420-110-DW', 'Programming I', 3,3,3,
        --Description
        'The course will introduce the student to the basic building blocks (sequential, selection and repetitive control structures) and modules (methods and classes) used to write a program. The student will use the Java programming language to implement the algorithms studied. The array data structure is introduced, and student will learn how to program with objects.',
        1, 1);
    --Competencies
    insert into competencies values ('00Q2', 'Use programming languages',
                                    '* For problems that are easily solved * Using basic algorithms * Using a debugger and a functional test plan',
                                    'Mandatory');                            
    insert into competencies values ('00Q3', 'Solve computer-related problems using mathematics',
                                    '* Based on situational problems * Using quantitative data',
                                    'Mandatory');
    insert into competencies values ('00Q4', 'Use office productivity software',
                                    '* Using word processing software, spreadsheet software, design software, presentation software and collaborative software * Using images, sounds and videos * Using presentation standards',
                                    'Mandatory');
    --Elements
        --00Q2
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 1,*/1, 'Analyze the problem.',
                                        '* Correct breakdown of the problem * Proper identification of input and output data and of the nature of the processes * Appropriate choice and adaptation of the algorithm',
                                        '00Q2');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 2,*/2, 'Translate the algorithm into a programming language.',
                                        '* Appropriate choice of instructions and types of elementary data * Efficient modularization of code * Logical organization of instructions * Compliance with the language syntax * Computer code consistent with the algorithm',
                                        '00Q2');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 3,*/3, 'Debug the code.',
                                        '* Efficient use of the debugger * Identification of all errors * Astute choice of debugging strategies * Relevance of the corrective actions * Clear record of solutions to the problems encountered',
                                        '00Q2');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 3,*/4, 'Implement the functional test plan.',
                                        '* Attitudes and behaviours that demonstrate thoroughness * Identification of all operational errors * Relevance of the corrective actions * Proper functioning of the program * Clear record of information concerning tests and their results',
                                        '00Q2');
        --00Q3
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 5,*/1, 'Process numbers as they are represented in the computer memory.',
                                        '* Accurate representation of numbers in different base systems * Accurate conversion of numbers from one base to another * Accurate interpretation of the ranges of numeric types * Accurate interpretation of the precision of numeric types * Appropriate choice of the numeric type',
                                        '00Q3');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 6,*/2, 'Represent two-dimensional geometric figures in the form of digital images.',
                                        '* Appropriate choice of instructions and types of elementary data * Efficient modularization of code * Logical organization of instructions * Compliance with the language syntax * Computer code consistent with the algorithm',
                                         '00Q3');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 7,*/3, 'Model multi-variable logical reasoning.',
                                        '* Efficient use of the debugger * Identification of all errors * Astute choice of debugging strategies * Relevance of the corrective actions * Clear record of solutions to the problems encountered',
                                        '00Q3');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 8,*/4, 'Process quantitative data using descriptive statistics.',
                                        '* Attitudes and behaviours that demonstrate thoroughness * Identification of all operational errors * Relevance of the corrective actions * Proper functioning of the program * Clear record of information concerning tests and their results',
                                         '00Q3');
        --00Q4
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 9,*/1, 'Produce reports.',
                                        '* Proper customizing of the word processing interface * Accurate data entry * Proper integration of images * Appropriate use and modification of styles and templates * Proper insertion of an automatic table of contents * Efficient use of the spelling and grammar check * Compliance with presentation standards',
                                         '00Q4');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 10,*/2, 'Produce tables and graphs.',
                                        '* Appropriate choice of instructions and types of elementary data * Efficient modularization of code * Logical organization of instructions * Compliance with the language syntax * Computer code consistent with the algorithm',
                                         '00Q4');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 11,*/3, 'Produce diagrams or plans.',
                                        '* Efficient use of the debugger * Identification of all errors * Astute choice of debugging strategies * Relevance of the corrective actions * Clear record of solutions to the problems encountered',
                                         '00Q4');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 12,*/4, 'Produce presentation documents.',
                                        '* Attitudes and behaviours that demonstrate thoroughness * Identification of all operational errors * Relevance of the corrective actions * Proper functioning of the program * Clear record of information concerning tests and their results',
                                         '00Q4');
    --course_elements
    insert into courses_elements values ('420-110-DW', 1/*GENERATED 1*/, (66/4));
    insert into courses_elements values ('420-110-DW', 2/*GENERATED 2*/, (66/4));
    insert into courses_elements values ('420-110-DW', 3/*GENERATED 3*/, (66/4));
    insert into courses_elements values ('420-110-DW', 4/*GENERATED 4*/, (66/4));
    insert into courses_elements values ('420-110-DW', 5/*GENERATED 5*/, (18/2));
    insert into courses_elements values ('420-110-DW', 7/*GENERATED 7*/, (18/2));
    insert into courses_elements values ('420-110-DW', 11/*GENERATED 11*/, 6);
    
--course with different term
--PROGRAMMING II----------------------------------------------------------------------------------------------------------------------
    --Term
    insert into terms values (2, 'Winter');
    --Domain
        --Same as Programming I
    --Course
    insert into courses values ('420-210-DW', 'Programming II', 3,3,3,
        --Description
        'The course will introduce the student to basic object-oriented methodology in order to design, implement, use and modify classes, to write programs in the Java language that perform interactive processing, array and string processing, and data validation. Object-oriented features such as encapsulation and inheritance will be explored.',
        1, 2);
    --Competencies
    --00Q2 same as programming I      00Q2
    insert into competencies values ('00Q6', 'Use an object-oriented development approach',
                                    '* Based on a problem * Using nomenclature and coding rules',
                                    'Mandatory');
    --Elements
        --00Q2 already declared
        --00Q6
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 13,*/1, 'Analyze the problem.',
                                        '* Breakdown of the problem based on the requirements of an object-oriented approach * Proper identification of input and output data and the nature of the processes * Accurate identification of the classes to be modelled * Proper identification of the algorithms to be created',
                                        '00Q6');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 14,*/2, 'Model the classes.',
                                        '* Proper identification of class attributes and methods * Proper application of encapsulation and inheritance principles * Proper graphic representation of the classes and their relationships * Compliance with nomenclature rules',
                                        '00Q6');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 15,*/3, 'Produce the algorithms for the methods.',
                                        '* Appropriate identification of the operations necessary for each method * Proper identification of a logical sequence of operations * Appropriate verification of algorithm correctness * Accurate representation of algorithms',
                                        '00Q6');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 16,*/4, 'Create the graphic interface.',
                                        '* Appropriate choice of graphic elements for display and data input * Proper layout of graphic elements * Proper set-up of graphic elements',
                                         '00Q6');
            --5.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 17,*/5, 'Program the classes.',
                                        '* Appropriate choice of instructions, types of primitive data and data structures * Logical organization of the instructions * Proper programming of messages to be displayed for the user * Proper integration of the classes into the program * Proper program performance * Compliance with the language syntax * Compliance with coding rules',
                                        '00Q6');
            --6.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 18,*/6, 'Document the code.',
                                        '* Clear comments in the computer code * Clear record of the programming support documentation * Appropriate use of the documentation generators',
                                        '00Q6');
    
    insert into courses_elements values ('420-210-DW', 1/*GENERATED*/, (45/4));
    insert into courses_elements values ('420-210-DW', 2/*GENERATED*/, (45/4));
    insert into courses_elements values ('420-210-DW', 3/*GENERATED*/, (45/4));
    insert into courses_elements values ('420-210-DW', 4/*GENERATED*/, (45/4));
    insert into courses_elements values ('420-210-DW', 13/*GENERATED*/, (45/5));
    insert into courses_elements values ('420-210-DW', 14/*GENERATED*/, (45/5));
    insert into courses_elements values ('420-210-DW', 15/*GENERATED*/, (45/5));
    insert into courses_elements values ('420-210-DW', 17/*GENERATED*/, (45/5));
    insert into courses_elements values ('420-210-DW', 18/*GENERATED*/, (45/5));
    
--course with different domain
--INFRASTRUCTURE III----------------------------------------------------------------------------------------------------------------------
    --Term
    insert into terms values (4, 'Winter');
    --Domain
    insert into domains values (2/*GENERATED*/, 'Infrastructure, Operating Systems and Networking',
        --Description
        'The courses within the Infrastructure, Operating Systems and Networking domain deliver the knowledge and skills required by the student to understand, install and optimally configure various operating systems locally or on the cloud, and to deploy and run applications on these systems.');
    --Course
    insert into courses values ('420-440-DW', 'Infrastructure III', 3,3,2,
        --Description
        'The course will use Linux to reinforce student understanding of web development and distributed systems. The characteristics of a multi-user, multitasking, multi-threaded operating system will be examined. Topics related to networking, security, monitoring,industry best practice authentication and directory services operations will be covered. Aspects of connectivity using TCP/IP protocols, and application services such as DNS, DHCP, SSH, and web servers with HTTP will be introduced. The students will also be introduced to virtual machine concepts and creation.',
        2, 4);
    --Competencies
    --00Q1
    insert into competencies values ('00Q1', 'Install and manage computers',
                                    '* For different operating systems * Based on a request * Using computers, peripheral devices, removable internal components, etc. * Using technical documents * Using operating systems, applications, utilities, drivers, plug-ins, etc.',
                                    'Mandatory');
    --00Q5
    insert into competencies values ('00Q5', 'Deploy a local computer network',
                                    '* For local wired and wireless computer networks * Based on a request * Using computers, interconnection devices and cabling * Using technical documentation',
                                    'Mandatory');
    --00Q8
    insert into competencies values ('00Q8', 'Carry out prevention operations with regard to information security',
                                    '* Using recognized security measures * Using information security software and encryption libraries',
                                    'Mandatory');
    --00SF
    insert into competencies values ('00SF', 'Evaluate software and hardware components',
                                    '* Using information sources * Based on functional specifications and architecture diagrams * Using technical documentation',
                                    'Mandatory');
    --00SH
    insert into competencies values ('00SH', 'Adapt to information technologies',
                                    '* Using information sources * Using computer applications and equipment',
                                    'Mandatory');
    --Elements
        --00Q1
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 19,*/1, 'Prepare the computer.',
                                        '* Accurate interpretation of the request * Accurate interpretation of the computer equipment specifications * Correct addition of removable components * Proper connection of peripheral devices * Ergonomic set-up of the computer and its peripheral devices',
                                        '00Q1');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 20,*/2, 'Install the operating system.',
                                        '* Appropriate use of file system preparation utilities * Proper installation of the operating systems and drivers * Proper configuration of the operating system and drivers * Customization of the operating system based on user needs',
                                        '00Q1');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 21,*/3, 'Install the applications.',
                                        '* Correct application of the procedure for installing the applications and plug-ins * Correct configuration of the applications and plug-ins * Customization of the applications and plug-ins based on user needs * Proper performance of the applications',
                                        '00Q1');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 22,*/4, 'Perform operating system management tasks.',
                                        '* Functional organization of the structure of files and directories * Appropriate use of archiving and compression software * Proper creation of user accounts and groups * Proper assignment of access rights * Appropriate management of processes, memory and disk space * Correct writing of scripts',
                                        '00Q1');
        --00Q5
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 23,*/1, 'Define the features of the local computer network.',
                                        '* Accurate interpretation of the request * Proper identification of the services to be installed * Appropriate choice of interconnection devices to be installed * Architecture diagram of the local network that meets the requirements',
                                         '00Q5');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 24,*/2, 'Install the local network interconnection devices.',
                                        '* Proper set-up and connection of the interconnection devices * Proper configuration of the interconnection devices * Clear record of the configurations carried out',
                                         '00Q5');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 25,*/3, 'Connect the computers to the local network.',
                                        '* Connection of the computers to the computer network according to the architecture diagram * Proper configuration of access to the network * Clear record of the configurations carried out',
                                         '00Q5');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 26,*/4, 'Install shared resource services.',
                                        '* Strict application of the procedure for installing services * Proper configuration of the services * Clear record of the configurations carried out',
                                         '00Q5');
            --5.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 27,*/5, 'Enable the local network.',
                                        '* Strict application of test plans * Relevance of the corrective actions * Optimal functioning of the network',
                                         '00Q5');
        --00Q8
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 28,*/1, 'Analyze information security risks.',
                                        '* Accurate inventory of the computing equipment and applications installed * Proper inventory of potential threats and vulnerabilities * Accurate identification of the impacts on security * Appropriate choice of security measures to be applied',
                                         '00Q8');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 29,*/2, 'Apply recognized security measures to protect the network.',
                                        '* Appropriate use of backup strategies * Appropriate use of strategies for assigning access rights * Proper configuration and customizing of anti-virus and firewall software * Appropriate use of encryption utilities',
                                         '00Q8');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 30,*/3, 'Apply recognized security measures to protect an application.',
                                        '* Appropriate use of strategies to secure data entered by users * Appropriate use of error control and exception management techniques * Appropriate use of secure authentication and authorizations mechanisms * Appropriate use of encryption libraries',
                                         '00Q8');
        --00SF
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 31,*/1, 'Pinpoint the technical requirements of a development or deployment project.',
                                        '* Accurate analysis of functional specifications * Accurate analysis of the software architecture and the computer network architecture * Identification of all technical requirements for the project',
                                         '00SF');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 32,*/2, 'Research software and hardware components.',
                                        '* Appropriate choice of information sources * Accurate inventory of the available software and hardware components',
                                         '00SF');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 33,*/3, 'Provide advice on software and hardware components.',
                                        '* Accurate analysis of the features of the platforms, applications and programming tools * Accurate analysis of the features of the computing devices, interconnection devices and peripheral devices * Accurate analysis of the features of the wired and wireless communications protocols * Relevance of advice on component compatibility * Relevance of advice on component longevity, efficiency and maintainability',
                                         '00SF');
        --00SH
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 34,*/1, 'Monitor technological developments.',
                                        '* Effective search for information sources * Appropriate use of monitoring tools * Accurate analysis of the information collected * Accurate identification of the technologies to test',
                                         '00SH');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 35,*/2, 'Test software and hardware technology.',
                                        '* Proper connection of computer equipment and the necessary peripheral devices * Proper installation of the necessary programming applications or tools * Adequate testing of the technology * Attitudes and behaviours that demonstrate self-reliance and open-mindedness',
                                         '00SH');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 36,*/3, 'Draw up technological opinions.',
                                        '* Active participation in discussions * Satisfactory justification of the technology?s potential',
                                         '00SH');
    
    --00Q1
    insert into courses_elements values ('420-440-DW', 20/*GENERATED*/, (9/3));
    insert into courses_elements values ('420-440-DW', 21/*GENERATED*/, (9/3));
    insert into courses_elements values ('420-440-DW', 22/*GENERATED*/, (9/3));
    --00Q5
    insert into courses_elements values ('420-440-DW', 23/*GENERATED*/, (30/5));
    insert into courses_elements values ('420-440-DW', 24/*GENERATED*/, (30/5));
    insert into courses_elements values ('420-440-DW', 25/*GENERATED*/, (30/5));
    insert into courses_elements values ('420-440-DW', 26/*GENERATED*/, (30/5));
    insert into courses_elements values ('420-440-DW', 27/*GENERATED*/, (30/5));
    --00Q8
    insert into courses_elements values ('420-440-DW', 28/*GENERATED*/, (18/2));
    insert into courses_elements values ('420-440-DW', 29/*GENERATED*/, (18/2));
    --00SF
    insert into courses_elements values ('420-440-DW', 31/*GENERATED*/, (12/3));
    insert into courses_elements values ('420-440-DW', 32/*GENERATED*/, (12/3));
    insert into courses_elements values ('420-440-DW', 33/*GENERATED*/, (12/3));
    --00SH
    insert into courses_elements values ('420-440-DW', 34/*GENERATED*/, (21/2));
    insert into courses_elements values ('420-440-DW', 36/*GENERATED*/, (21/2));

--course with hours that don't match up
--DATABASE I----------------------------------------------------------------------------------------------------------------------
--Term
    --already made with programming II
    --Domain
    insert into domains values (3/*GENERATED*/, 'Database',
        --Description
        'The Database domain courses give the student the knowledge and skills to build relational databases and to administer a database management system. This domain will draw upon the knowledge and skills learned in the programming, data structures and algorithms domain.');
    --Course
    insert into courses values ('420-231-DW', 'Database I', 3,7/*WRONG VALUE supposed to be 3*/,3,
        --Description
        'The course will teach tools and techniques for database design and the use of
Structured Query Language (SQL). This course will cover the fundamental
concepts of the relational data model; the use of selected data modeling
methodologies; and data normalization techniques to create robust relations.',
        3, 2);
    --Competencies
    --Uses 00Q2                   
    insert into competencies values ('00Q7', 'Use a database management system.',
                                    '* For a relational or other type of database management system * Based on the data model and specifications of the database management system',
                                    'Mandatory');
    --Elements
        --00Q7
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 37,*/1, 'Create the database.',
                                        '* Accurate analysis of the data model
* Accurate analysis of the specifications of the database management system
* Appropriate coding of the instructions for creating the database',
                                        '00Q7');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 38,*/2, 'Formulate read requests, insertion requests, modification requests and deletion requests.',
                                        '* Accurate identification of the types of requests to be formulated
* Appropriate use of clauses, operators, commands and parameters
* Appropriate use of regular expressions
* Proper performance of requests',
                                        '00Q7');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 39,*/3, 'Ensure data confidentiality and consistency.',
                                        '* Accurate identification of the techniques to be used
* Proper management of authorizations
* Appropriate data encryption
* Appropriate use of referential integrity constraints, triggers and transactions',
                                        '00Q7');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 40,*/4, 'Program automated data processing operations.',
                                        '* Accurate identification of data processing operations to be automated
* Appropriate creation of stored procedures and scripts
* Clear record of programming support documentation',
                                        '00Q7');
            --5.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 41,*/5, 'Save and restore the database.',
                                        '* Astute choice of techniques to be used for saving and restoring
* Appropriate use of techniques for saving and restoring the database
* Compliance with the procedure and frequency for saving the database',
                                        '00Q7');
    --course_elements
    insert into courses_elements values ('420-231-DW', 1/*GENERATED 1*/, (30/2));
    insert into courses_elements values ('420-231-DW', 2/*GENERATED 2*/, (30/2));
    insert into courses_elements values ('420-231-DW', 37/*GENERATED 37*/, (60/5));
    insert into courses_elements values ('420-231-DW', 38/*GENERATED 38*/, (60/5));
    insert into courses_elements values ('420-231-DW', 39/*GENERATED 39*/, (60/5));
    insert into courses_elements values ('420-231-DW', 40/*GENERATED 40*/, (60/5));
    insert into courses_elements values ('420-231-DW', 41/*GENERATED 41*/,(60/5));
    
--course with bad course id
--MOBILE DEVELOPMENT----------------------------------------------------------------------------------------------------------------------
--Term
    insert into terms values (5, 'Fall');
    --Domain
    --same domain as programming I and II
    --Course
    insert into courses values ('420-551-D', 'Mobile Development', 3,3,3,
        --Description
        'The course will focus on the development of applications within the Android
environment. Students will learn how to analyze, design, construct, and
implement an e?ective mobile application using the Android mobile
development environment.',
        1, 5);

    --Uses 00SR
    --Uses 00SS
    insert into competencies values ('00SR', 'Develop native applications without a database.',
                                    '* For different target platforms: tablets, smartphones, desktop computers, etc.
* For new applications and applications to be modified
* Based on design documents
* Using a compiler designed for the target platform, a cross compiler or an interpreter
* Using an emulator on the development platform
* Using images, sounds and videos
* Using issue tracking and version control procedures',
                                    'Mandatory');
    insert into competencies values ('00SS', 'Develop native applications with a database.',
                                     '* For different target platforms: tablets, smartphones, desktop computers, etc.
* For new applications and applications to be modified
* Based on design documents
* Using a compiler designed for the target platform, a cross compiler or an interpreter
* Using an emulator on the development platform
* Using images
* Using issue tracking and version control procedures',
                                    'Mandatory');
    --Elements
        --00SR
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 38,*/1, 'Analyze the application development project.',
                                        '* Accurate analysis of design documents
* Proper identification of tasks to be carried out',
                                        '00SR');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 39,*/2, 'Prepare the computer development environment.',
                                        '* Proper installation of software and libraries on the development platform
* Proper configuration of the target platform
* Proper configuration of the version control system
* Proper importing of the source code',
                                        '00SR');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 40,*/3, 'Generate or program the graphical interface.',
                                        '* Appropriate choice and use of graphic elements for display and input
* Proper integration of images
* Adaptation of the interface based on the display format and resolution',
                                        '00SR');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 41,*/4, 'Program the application logic.',
                                        '* Proper programming of interactions between the graphical user interface and the user
* Proper programming of communications between the peripheral devices and the software functions of the target platform
* Effective use of execution threads
* Proper integration of sounds and videos
* Proper application of internationalization techniques
* Precise application of secure coding techniques',
                                        '00SR');
            --5.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 42,*/5, 'Control the quality of the application.',
                                        '* Precise application of test plans in the emulator and on the target platform
* Thorough reviews of code and security
* Relevance of the corrective actions
* Compliance with issue tracking and version control procedures
* Compliance with design documents',
                                        '00SR');
        --00SS
            --1.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 43,*/1, 'Analyze the application development project.',
                                        '* Accurate analysis of design documents
* Proper identification of the tasks to be carried out',
                                        '00SS');
            --2.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 44,*/2, 'Prepare the computer development environment.',
                                        '* Proper installation of software and libraries on the development platform
* Proper configuration of the target platform
* Proper configuration of the version control system
* Proper importing of the source code',
                                        '00SS');
            --3.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 45,*/3, 'Prepare the database(s).',
                                        '* Proper creation or adaptation of the local or remote database
* Proper insertion of initial or test data
* Compliance with the data model',
                                        '00SS');
            --4.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 46,*/4, 'Generate or program the graphical user interface.',
                                        '* Appropriate choice and use of graphic elements for display and input
* Proper integration of images
* Adaptation of the interface based on the display format and resolution',
                                        '00SS');
            --5.
            insert into elements (element_order, element, element_criteria, competency_id)
                                        values (/*GENERATED 47,*/5, 'Program the application logic.',
                                        '* Proper programming or integration of authentication and authorization mechanisms
* Proper programming of interactions between the graphical user interface and the user
* Appropriate choice of clauses, operators, commands or parameters in database queries
* Correct handling of database data
* Proper programming of data synchronization
* Appropriate use of data exchange services
* Proper application of internationalization techniques
* Precise application of secure programming techniques',
                                        '00SS');
    --course_elements
    insert into courses_elements values ('420-551-D', 38/*GENERATED 38*/, (45/5));
    insert into courses_elements values ('420-551-D', 39/*GENERATED 39*/, (45/5));
    insert into courses_elements values ('420-551-D', 40/*GENERATED 40*/, (45/5));
    insert into courses_elements values ('420-551-D', 41/*GENERATED 41*/, (45/5));
    insert into courses_elements values ('420-551-D', 42/*GENERATED 42*/, (45/5));
    insert into courses_elements values ('420-551-D', 43/*GENERATED 43*/, (45/5));
    insert into courses_elements values ('420-551-D', 44/*GENERATED 44*/,(45/5));
    insert into courses_elements values ('420-551-D', 45/*GENERATED 45*/,(45/5));
    insert into courses_elements values ('420-551-D', 46/*GENERATED 46*/,(45/5));
    insert into courses_elements values ('420-551-D', 47/*GENERATED 47*/,(45/5));

--additional term inserts
insert into terms values (3, 'Fall');
insert into terms values (6, 'Winter');
