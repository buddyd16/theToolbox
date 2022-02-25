# theToolbox
Portions of the code used to run the toolbox website


Site Specific Roadmap:
- [x] Rorganize to use Flask Blueprint System
- [ ] Database implementation for User logins with the intial purpose of allowing calculations to be saved 

Tools Roadmap
- [ ] Multi-span Beam Analysis inclusive of load combinations and patterning
  - [ ] Python Backend Methods
    - [x] Load Combination Class
    - [x] Load Pattern Generator Functions
    - [x] Beam Load functions
    - [x] Flexibility Method Solver
    - [x] Beam Class to pull it all together and store data as attributes to make access easier on the web side
    - [x] Data pre-processor to churn through all the form data and organize it to fit the calculation models
    - [x] Computation model
    - [ ] function in the beam class to envelope reactions for web display
  - [ ] HTML Template
    - [x] Generalized Input to accept a list of inputs for repopulation of inputs after a POST method
    - [ ] Layout for ULS Results
    - [ ] Layout for SLS Results
    - [ ] Layout for Basic Results 
    - [x] Javascript to plot the applied loads on the geometry canvas
- [ ] Retaining wall inclusive of allowing numerous user defined loads in addition to the typical soil and surcharge loads seen in these tools, don't know about anyone else but brick veneer, wind concentrated, and wind distributed loads are a common occurance that no software packages seem to address.
- [ ] Wood Stud Walls
- [ ] Strap Beam
- [ ] Rigid Diaphragm -- Single floor diaphgragm to be expanded to cover multiple floors and check for irregularities
- [ ] Biaxial Rectangular Concrete Column - short columns first slender to follow
- [ ] Biaxial Circular Concrete Column - short columns first slender to follow
- [ ] and many more!
- [ ] Units! 
- [ ] Other National Codes

I'm not sure when any of this is going to get done but I'm giong to enjoy the ride.
