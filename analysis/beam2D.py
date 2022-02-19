import geometry2D

class Beam2D():
    '''
    A class representing a 2D - Euler-Bernoulli Beam
    '''

    def __init__(self, userName, node_i, node_j, Em, Ixx, endCondition=[0, 0]):

        self.userName = userName            # User defined name
        self.node_i = node_i                # Beam i node (x,y)
        self.node_j = node_j                # Beam j node (x,y)
        self.Em = Em                        # Beam modulus of elasticity
        self.Ixx = Ixx                      # Beam moment of inertia about
                                            # the axis of bending
        self.endCondition = endCondition    # Beam end condition 1-fixed 0-pin

        # Initiliaze empty data sets for other variable beam info
        self.interiorSupports = []  # List of additional support locations, as a 
                                    # relative distance from the i end along beam.
        self.loads = []             # List to hold the applied loads
        self.reactions_basic = {}   # List to hold Basic reactions
        self.reactions_uls = {}     # List to hold ULS reactions
        self.reactions_sls = {}     # List to hold Service Reactions
        self.Mu_max = []            # List to hold Mu,max (ULS Moment Envelope)
        self.Mu_min = []            # List to hold Mu,min (ULS Moment Envelope)
        self.Vu_max = []            # List to hold Vu,max (ULS Shear Envelope)
        self.Vu_min = []            # List to hold Vu,min (ULS Shear Envelope)
        self.Ms_max = []            # List to hold Ms,max (Service Moment Envelope)
        self.Ms_min = []            # List to hold Ms,min (Service Moment Envelope)
        self.Vs_max = []            # List to hold Vs,max (Service Shear Envelope)
        self.Vs_min = []            # List to hold Vs,min (Service Shear Envelope)
        self.S_min = []             # List to hold Slope,min (Service Envelope)
        self.S_max = []             # List to hold Slope,max (Service Envelope)
        self.D_min = []             # List to hold Deflection,min (Service Envelope)
        self.D_max = []             # List to hold Deflection,max (Service Envelope)

    @property
    def span(self):
        '''
        Compute the length of the beam
        '''

        x1 = self.node_i.x
        y1 = self.node_i.y
        x2 = self.node_j.x
        y2 = self.node_j.y

        self._span = (((x2-x1)**2)+((y2-y1)**2))**0.5

        return self._span

    def addinteriorsupport(self, location):
        '''
        Add an interior support to the beam interiorSupports list
        '''

        self.interiorSupports.append(location)

    def addLoads(self, newLoads):
        '''
        newLoads = []  list of load classes

        Loads should already be converted to one of the load class types
        prior to adding them to the beam
        '''

        self.loads.extend(newLoads)

    def spans(self):
        '''
        compute the list of spans making up the total beam span
        considering interior supports.

        returns a list of floats   [s1,...,si]
        '''
        
        spans = []
        
        if self.interiorSupports == []:
            spans.append(self.span)
        else:
            for i, support in enumerate(self.interiorSupports):
                
                if i == 0:
                    spans.append(support)
                else:
                    spans.append(support-self.interiorSupports[i-1])
            
            spans.append(self.span - self.interiorSupports[-1])
        
        return spans

    def computation_stations(self, num_stations=26):
        '''
        define general computation points along the beam length for shear,
        moment, slope, and deflection plots
        '''
        extra_stations = []
        
        
        'paramtric list of stations between 0 and 1'
        eta = [0+i*(1/num_stations) for i in range(num_stations+1)]

        if self.interiorSupports == []:
            stations = [self.span*i for i in eta]

        else:

            stations = []

            spans = self.spans()

            for j,span in enumerate(spans):

                if j == 0:
                    stations.extend([span*i for i in eta])
                else:
                    stations.extend([stations[-1] + span*i for i in eta])
            
            for support in self.interiorSupports:
                
                extra_stations.append(support-0.001)
                extra_stations.append(support+0.001)

        # Loop through the applied loading and generate calculation points
        # at start and ends of distributed loadings and at point loadings
        # include an additional point at a small tolerance before and after
        # each location to ensure diagram discontinuities are captured.
        Loads = self.loads

        
        
        if Loads == []:
            pass
        else:
            for load in self.loads:

                if load.kind == 'POINT' or load.kind=='MOMENT':
                    b = min(self.span, load.a + 0.001)
                    c = max(0, load.a - 0.001)
                    extra_stations.extend([c, load.a, b])

                elif load.kind == 'UDL' or load.kind=='TRAP':
                    c = min(self.span, load.b+0.001)
                    d = max(0, load.a-0.001)
                    extra_stations.extend([d, load.a, load.b, c])
                else:
                    pass

        stations.extend(extra_stations)

        stations.sort()

        # Make sure the first and last stations do not exceed the beam

        if stations[0] < 0:
            stations[0] = 0

        if stations[-1] > self.span:
            stations[-1] = self.span

        # Remove duplicate locations

        self.calcstations = list(set(stations))
        self.calcstations.sort()


# Test Area #

n1 = geometry2D.Node2D(0, 0, "N1", 1)
n2 = geometry2D.Node2D(30, 0, "N2", 2)

print(n1)
print(n2)

beam = Beam2D("BM1", n1, n2, 29000, 30.8)

beam.addinteriorsupport(10.3)
beam.addinteriorsupport(19.5)

print(beam.spans())

beam.computation_stations()

print(beam.calcstations)