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











