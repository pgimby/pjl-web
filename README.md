# pjl-web
### Document dump for the PJL at UofC



## **To Do List**

XML validation (done)  
PHP to handle database edit POSTS (investigate Apache mod for Python)  
Refine site-wide/page-specific scripts and stylesheets and implement page-specific JS namespaces (dashboard done - repo not done)  
Dashboard to edit XMLs (in progress)  
Populate equipment tags in lab XML (final draft done - awaiting Peter's review)  
Populate topics / disciplines / ID#s (in progress)  
Add legacy labs (done)  
Student guide  
Support docs  
External references (done)  
Companion guides  
325 final project ideas  



## **Pages to add**

Landing page  
Repository (alpha finished)  
Equipment page template with URL string queries  
Database editing dashboard(s) (in progress)  
Staff profiles  
Room scheduling interactive map (SVG ready to go)  
Demos repository (unconfirmed)  
403, 404, 500, 503 HTTP error pages  


# Site Map

<img src="/dev/sitemap.png" width="480">

# Source Map

<img src="/dev/sourcemap.png" width="480">


# Lab Meta Data


## **Disciplines**  
###### Labs are identified with disciplines when the discipline constitutes a significant focus of the lab

<!---start disciplines-->
Newtonian Mechanics  
Electricity and Magnetism  
Optics  
Thermodynamics  
Fluid Mechanics  
Statistical Mechanics  
Quantum Mechanics  
Relativity  
Particle Physics  
Nuclear Physics  
Math  
Laboratory Skills  
Computer Skills  
<!---end disciplines-->


## **Topics**  
###### Labs are identified with topics when the topic constitutes a significant focus of the lab or if the topic is an explicitly necessary pre-requisite

<!---start topics-->
Electrostatics  
Circuits  
PDE  
ODE  
Statistics  
Linear Algebra  
Integration  
Differentiation  
Rotational Motion  
Statics  
Kinematics  
Collisions  
Dynamics  
Measurements  
Work and Energy  
Friction and Drag  
Momentum  
Conservation Laws  
Magnetism  
Interference  
Polarization  
Newton’s Laws  
Wave Mechanics  
Malus' Law  
Refraction
<!---end topics-->



# Database Templates

## **Lab XML Template**


```
<Labs>
    <Lab labId="0001">
        <Name />
        <Disciplines>
            <Discipline />
            ...
        </Disciplines>
        <Topics>
            <Topic />
            ...
        </Topics>
        <Versions>
            <Version>
                <Path />
                <Semester />
                <Year />
                <Course />
            </Version>
            ...
        </Versions>
        <Equipment>
            <Item id="0001">
                <Name />
                <Amount />
            </Item>
            ...
        <Equipment />
        <Type />
        <SupportDocs>
            <Doc>
                <Name />
                <Path />
            </Doc>
            ...
        </SupportDocs>
        <Software>
            <Name />
            ...
        </Software>
    </Lab>
    ...
</Labs>

```


## **Equipment XML Template**

```
<Equipment>
    <Item id="0001">
        <InventoryName />
        <Identification>
            <Manufacturer />
            <Model />
        </Identification>
        <Location>
            <Room />
            <Storage />
        </Location>
        <Quantity>
            <Total />
            <InService />
            <UnderRepair />
        </Quantity>
        <Documents>
            <Document>
                <Name />
                <location>
                    <Online />
                    <Offline />
                </location>
            </Document>
            ...
        </Documents>
    </Item>
    ...
</Equipment>
```


#  pjlDB.py Documentation


## Convenience Functions

##### pjlDB.isValidID(idnum)
> Checks if idnum is a valid ID number. Returns True if valid, False if not.


##### pjlDB.getTopics()
> Returns a list of valid topics taken from the pjl-web README.


##### pjlDB.getDisciplines()
> Returns a list of valid disciplines taken from the pjl-web README.






## pjlDB.labDB


### Properties

##### labDB.tree
> An `xml.etree.ElementTree.ElementTree` object for the database being held.


##### labDB.root
> An `xml.etree.ElementTree.Element` object that is the root element of labDB.tree.


##### labDB.labs
> a list of `_labItem` objects. All the properties and methods of this class are described below.


##### labDB.new_id
> This will always return the next available unused lab ID in the appropriate string form.


##### labDB.length
> This will always return the current number of labs in the held database.



### Methods

##### labDB.newLab(idnum)
> Returns an empty `_labItem` object with lab ID set to `idnum`. Throws an exception if `idnum` is not a valid form or if `idnum` already exists in the database.


##### labDB.getLab(idnum=None, name=None)
> Returns a `_labItem` object belonging to either `idnum` or `name`. Either lab ID or lab name may be used to access one of the labs in the database. Throws an exception if a matching lab cannot be found or if invalid arguments are passed.


##### labDB.addLab(labitem)
> Adds a `_labItem` object to the held database. If an identical lab already exists, it is replaced. If it does not already exist, a new lab entry is appended to the held database.


##### labDB.save(filename, ignore_validation=False, error_log=False)
> Saves the database as an XML file with UTF-8 encoding. If `ignore_validation` is True, `labDB` will attempt to write the XML without any validation of its contents. If False, a full validation will be performed before writing. If `error_log` is True, an error report will be saved to the working directory. If False, the error log will be printed to the console.


##### labDB.validateFull(error_log=False)
> Performs a full validation of the database being held. If `error_log` is True, the error log is written to a file in the working directory. If False, the error log is printed to the console.


##### labDB.noDuplicateIDs(log=None)
> Checks if the database contains any duplicate lab IDs. Returns True if no duplicates found, False if duplicates found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.


##### labDB.hasUniqueEquipIDs(log=None)
> Checks if the database contains any non-unique equipment IDs. Returns True if none found, False if found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.


##### labDB.hasValidPathRoots(log=None)
> Checks if the database contains any improper directory roots. Returns True if no improper paths found, False if found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.


##### labDB.hasValidTopics(log=None)
> Checks for invalid topics. Returns True if no invalid topics found, False if any found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.


##### labDB.hasValidDisciplines(log=None)
> Checks for invalid disciplines. Returns True if no invalid disciplines found, False if any found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.


##### labDB.hasValidTypes(log=None)
> Checks for invalid lab types. Returns True if no invalid types found, False if any found. if `log` is None then error log is printed to the console. If a file object is passed as an argument then the error log is written to that file.





## pjlDB.labItem
> Used by `labDB` objects to store lab items. Type checking and validation of its properties is performed by the `labDB` object.

### Properties

##### labItem.id_num
> A string holding an integer between 0001 and 9999 inclusive. These are ID numbers and are unique to each lab.


##### labItem.name
> A string representing the name of a lab.


##### labItem.disciplines
> A list of strings representing valid disciplines associated with a lab. Valid disciplines are those listed in the pjl-web README.


##### labItem.topics
> A list of strings representing valid topics associated with a lab. Valid topics are those listed in the pjl-web README.


##### labItem.versions
> A list of dictionaries representing individual versions. Each dictionary has 4 keys: "path", "semester", "year", and "course".  
>  
> Ex.  
> {"path:"/data/repository/path/to/file.pdf", "semester":"Fall", "year" : "2012", "course":"PHYS 397"}


##### labItem.equipment
> A list of dictionaries representing individual equipment items. Each dictionary has 3 keys: "id", "name", and "amount".  
>  
> Ex.  
> {"id":"0001", "name":"Fluke multimeter", "amount" : "2"}


##### labItem.lab_type
> A string containing either "Lab" or "Labatorial" representing the type of the lab.


##### labItem.support_docs
> A list of dictionaries representing individual documents. Each dictionary has 2 keys: "name" and "path".  
>  
> Ex.  
> {"name":"Hugo's notes", "path":"/data/repository/path/to/file.pdf"}


##### labItem.software
> A list of strings representing required software, libraries, or files for a lab.





### Methods
> Object has no methods...yet








