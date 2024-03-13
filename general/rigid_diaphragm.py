import math
import numpy as np


class lateral_element:
    def __init__(self, location=[0, 0], rotation_degrees = 0, kstrong=1, kweak=0):

        self.location = location
        self.x = location[0]
        self.y = location[1]

        self.kstrong = kstrong
        self.kweak = kweak
        self.rotation_degrees = rotation_degrees

        self.analysis_results = {}

    def set_rotation_degrees(self, rotation_degrees):
        self.rotation_degrees = rotation_degrees

    def set_stiffness(self, k, axis=1):
        if axis == 1:
            self.kstrong = k
        elif axis == 2:
            self.kweak = k
        else:
            raise Exception("Axis must be either 1 for Strong or 2 for Weak")

    def set_stiffness_from_unit_load_deflection(self, delta, axis=1):

        if axis == 1:
            self.kstrong = 1 / delta

        elif axis == 2:
            self.kweak = 1 / delta

        else:
            raise Exception("Axis must be either 1 for Strong or 2 for Weak")

    def T(self):
        # Transformation matrix to transition from local to global coordinate systems
        rotation_rad = math.radians(self.rotation_degrees)
        s = math.sin(rotation_rad)
        c = math.cos(rotation_rad)

        T = np.array([[c, s, 0, 0], [-1 * s, c, 0, 0], [0, 0, c, s], [0, 0, -1 * s, c]])

        return T

    def Klocal(self):
        ks = self.kstrong
        kw = self.kweak

        Klocal = np.array(
            [
                [ks, 0, -1 * ks, 0],
                [0, kw, 0, -1 * kw],
                [-1 * ks, 0, ks, 0],
                [0, -1 * kw, 0, kw],
            ]
        )

        return Klocal

    def Kglobal(self):
        # The full elastic stiffness matrix in reference to the global coordinate system.
        k = self.Klocal()
        T = self.T()

        Kglobal = np.matmul(np.matmul(np.transpose(T), k), T)

        return Kglobal

    def Kdiaphragm(self):
        # The reduced elastic stiffness matrix for the diaphragm plane
        Kglobal = self.Kglobal()

        Kdiaphragm = np.array(
            [[Kglobal[2][2], Kglobal[2, 3]], [Kglobal[3][2], Kglobal[3][3]]]
        )

        return Kdiaphragm

    def Kprime(self, reference_point=[0, 0]):
        dx = self.x - reference_point[0]
        dy = self.y - reference_point[1]

        Kdiaphragm = self.Kdiaphragm()

        k11 = Kdiaphragm[0][0]
        k12 = Kdiaphragm[0][1]
        k21 = Kdiaphragm[1][0]
        k22 = Kdiaphragm[1][1]

        k13 = (k12 * dx) - (k11 * dy)
        k23 = (k22 * dx) - (k21 * dy)
        k31 = k13
        k32 = k23
        k33 = (dy * dy * k11) + (dx * dx * k22) - (2 * dx * dy * k12)

        Kprime = np.array([[k11, k12, k13], [k21, k22, k23], [k31, k32, k33]])

        return Kprime

    def _element_results(self, case="None", reference_point=[0,0], deformation=[0,0,0]):

        case = case

        kprime = self.Kprime(reference_point)

        # Forces from f = kd
        Fbasic = np.matmul(kprime, deformation)

        # Direct Forces in the global axis
        kdirect = kprime[0:2,0:2]
        ddirect = deformation[0:2,:]

        Fdirect = np.matmul(kdirect, ddirect)

        # Forces from Torsion in the global axis
        ktorsion = kprime[0:2,-1]

        Ftorsion = ktorsion * deformation[-1]
        Ftorvect = Ftorsion.reshape(2,1)

        # Forces in the Local Axis
        T = self.T()

        Treduced = T[2:,2:]

        
        Fdirect_local = np.matmul(Treduced,Fdirect)
        Ftorsion_local = np.matmul(Treduced,Ftorvect)
        Flocal = np.add(Fdirect_local,Ftorsion_local)

        # Deflection in the global axis considering Torsion
        dx = self.x - reference_point[0]
        dy = self.y - reference_point[1]

        position_matrix = np.array([
            [dx],
            [dy]
        ])

        c = math.cos(deformation[-1][0])
        s = math.sin(deformation[-1][0])

        rot_matrix = np.array([
            [c, -1*s],
            [s, c]
        ])

        rotated_position = np.matmul(rot_matrix, position_matrix)
        delta_torsion = np.subtract(rotated_position, position_matrix)
        delta_direct = deformation[0:2]
        delta_global = np.add(delta_torsion,delta_direct)

        # Local force is the negative of the spring forces determined
        self.analysis_results[case] = {
            "Fglobal": Fbasic,
            "Fdirect_global": Fdirect,
            "Ftorsion_global": Ftorvect,
            "Flocal": -1*Flocal,
            "Fdirect_local": -1*Fdirect_local,
            "Ftorsion_local": -1*Ftorsion_local,
            "Delta_global": delta_global,
            "Delta_direct": delta_direct,
            "Delta_torsion": delta_torsion
        }



class rigid_diaphragm:
    def __init__(self, lateral_elements=[]):

        self.lateral_elements = lateral_elements

        self.COR = [0,0]

        self.applied_forces = {}

        self.displacements = {}

        self.analysis_results = {}

        #flags
        self._COR_determined = False

    def add_lateral_element(self, element):

        self.lateral_elements.append(element)

        self._COR_determined = False
    
    def remove_element_at_index(self, element_index):

        del self.lateral_elements[element_index]

        self._COR_determined = False
    
    def add_force_set(self, case="basic", FxFyMz = [1,1,1], location=[0,0]):

        if case in self.applied_forces:
            print(f"Load case {case} exist already, will append 1 and add anyway")
            case += "1"
        
        self.applied_forces[case] = {"load": FxFyMz, "location": location}


    def Ksystem(self, reference_point=[0,0]):

        Ksystem = np.zeros([3,3])
        
        for element in self.lateral_elements:

            Ksystem += element.Kprime(reference_point)
        
        return Ksystem

    def center_of_rigidity(self):

        if not self._COR_determined:
            Kcr = self.Ksystem([0,0])

            eq1 = np.array([
                [Kcr[0][0],Kcr[0][1]],
                [Kcr[1][0],Kcr[1][1]]
            ])

            sol1 = np.array([
                [Kcr[0][2]],
                [Kcr[1][2]]
            ])

            cr_xy = np.linalg.solve(eq1, sol1)

            center_of_rigidty = [cr_xy[1][0],-1*cr_xy[0][0]]

            self._COR_determined = True
            self.COR = center_of_rigidty
        
        else:
            print("COR already Determined echoing previous result")
            center_of_rigidty = self.COR

        return center_of_rigidty

    def diapraghm_analysis_about_cor(self, case="None"):

        if not self._COR_determined:
            self.center_of_rigidity()

        if case in self.applied_forces:

            load_data = self.applied_forces.get(case, 0)

            if load_data == 0:
                raise Exception("Something Went Wrong When Trying to Get the Load Data")

            else:

                load_set = load_data.get("load", [0,0,0])
                load_location = load_data.get("location", "COR")

                if load_location == "COR":
                    load_location = self.COR
                
                load_dx = load_location[0] - self.COR[0]
                load_dy = load_location[1] - self.COR[1]

                Fx = load_set[0]
                Fy = load_set[1]
                Mz = (Fy*load_dx)+(-1*Fx*load_dy)+load_set[2]

                Load_at_COR = np.array([
                    [Fx],
                    [Fy],
                    [Mz]
                ])

                Ksystem = self.Ksystem(self.COR)

                D = np.linalg.solve(Ksystem,Load_at_COR)

                # Element Force Recovery
                for element in self.lateral_elements:
                    element._element_results(case,self.COR, D)
                
                # Check Statics
                Fxx = 0
                Fyy = 0 
                Mzz = 0 
                for element in self.lateral_elements:
                    element_result = element.analysis_results.get(case, 0)

                    if element_result == 0:
                        raise Exception(f"Error in element force recovery in statics check for case: {case}!")
                    else:
                        Felement = element_result.get("Fglobal",[[0],[0],[0]])
                        Fxx += Felement[0][0]
                        Fyy += Felement[1][0]
                        Mzz += Felement[2][0]
                
                # checking against 0 but isclose function can get tripped up here
                # so take the difference and add 1 and compare to 1 to avoid
                # tolerance issues with 0
                Fx_check = math.isclose((Fx-Fxx)+1, 1)
                Fy_check = math.isclose((Fy-Fyy)+1, 1)
                Mzz_check = math.isclose((Mz-Mzz)+1,1)

                self.analysis_results[case] = {
                    "Forces at COR": Load_at_COR,
                    "D": D,
                    "Statics_check": {"status": all([Fx_check, Fy_check, Mzz_check]),
                                        "sumFx": Fxx,
                                        "sumFy": Fyy,
                                        "sumMz": Mzz}
                }

        else:
            raise Exception(f"No applied loads for passed in case of {case}!")

def print_results(diaphragm, lateral_elements, case):
    output_string = []

    case = "C1"

    output_string.append("-"*100)
    output_string.append(f"Diaphragm results for case {case} : ")
    output_string.append(f"Center of Rigiditiy: ( {diaphragm.COR[0]:^10.3f}, {diaphragm.COR[1]:^10.3f})")

    results = diaphragm.analysis_results.get(case, 0)

    if results == 0:
        output_string.append("Diaphragm results for case {case} not found.")
    else:
        output_string.append(f"{'':^20}|{'Fx':^20}|{'Fy':^20}|{'Mz':^20}|")
        output_string.append(f"{'Forces at COR':^20}|{results.get('Forces at COR')[0][0]:^20.3f}|{results.get('Forces at COR')[1][0]:^20.3f}|{results.get('Forces at COR')[2][0]:^20.3f}|")
        output_string.append("-"*100)
        output_string.append(f"Statics Check: {results.get('Statics_check').get('status')}")
        output_string.append(f"{'':^20}|{'sum Fx':^20}|{'sum Fy':^20}|{'sum Mz':^20}|")
        output_string.append(f"{'':^20}|{results.get('Statics_check').get('sumFx'):^20.3f}|{results.get('Statics_check').get('sumFy'):^20.3f}|{results.get('Statics_check').get('sumMz'):^20.3f}|")
        output_string.append("-"*100)
        output_string.append("Deformation of the COR: ")
        output_string.append(f"{'':^20}|{'Dx':^20}|{'Dy':^20}|{'Rz':^20}|")
        output_string.append(f"{'':^20}|{results.get('D')[0][0]:^20.4E}|{results.get('D')[1][0]:^20.4E}|{results.get('D')[2][0]:^20.4E}|")

    for i, element in enumerate(lateral_elements):
        output_string.append("-"*100)
        output_string.append(f"Lateral Element {i+1} Results for case {case} : ")

        element_results = element.analysis_results.get(case, 0)

        if element_results == 0:
            output_string.append(f"Element results for case {case} not found.")
        else:
            output_string.append("-"*100)
            output_string.append(f"{'Element Local Forces':^30}|{'Fs':^20}|{'Fw':^20}|")
            output_string.append(f"{'F':^30}|{element_results.get('Flocal')[0][0]:^20.4E}|{element_results.get('Flocal')[1][0]:^20.4E}|")
            output_string.append(f"{'F,direct':^30}|{element_results.get('Fdirect_local')[0][0]:^20.4E}|{element_results.get('Fdirect_local')[1][0]:^20.4E}|")
            output_string.append(f"{'F,torsion':^30}|{element_results.get('Ftorsion_local')[0][0]:^20.4E}|{element_results.get('Ftorsion_local')[1][0]:^20.4E}|")
            output_string.append("-"*100)
            output_string.append(f"{'Element Global Forces':^30}|{'Fx':^20}|{'Fy':^20}|")
            output_string.append(f"{'F':^30}|{element_results.get('Fglobal')[0][0]:^20.4E}|{element_results.get('Fglobal')[1][0]:^20.4E}|")
            output_string.append(f"{'F,direct':^30}|{element_results.get('Fdirect_global')[0][0]:^20.4E}|{element_results.get('Fdirect_global')[1][0]:^20.4E}|")
            output_string.append(f"{'F,torsion':^30}|{element_results.get('Ftorsion_global')[0][0]:^20.4E}|{element_results.get('Ftorsion_global')[1][0]:^20.4E}|")
            output_string.append("-"*100)
            output_string.append(f"{'Element Global Deformation':^30}|{'Dx':^20}|{'Dy':^20}|")
            output_string.append(f"{'Total':^30}|{element_results.get('Delta_global')[0][0]:^20.4E}|{element_results.get('Delta_global')[1][0]:^20.4E}|")
            output_string.append(f"{'Direct':^30}|{element_results.get('Delta_direct')[0][0]:^20.4E}|{element_results.get('Delta_direct')[1][0]:^20.4E}|")
            output_string.append(f"{'Torsion':^30}|{element_results.get('Delta_torsion')[0][0]:^20.4E}|{element_results.get('Delta_torsion')[1][0]:^20.4E}|")
        
    return output_string

if __name__ == "__main__":

    wall1 = lateral_element([0, 5],90,8.577e4,1.456e3)
    wall2 = lateral_element([20, 5],90,8.577e4,1.456e3)
    wall3 = lateral_element([40, 5],90,8.577e4,1.456e3)
    wall4 = lateral_element([60, 5],45,8.577e4,1.456e3)

    lateral_elements = [wall1,wall2,wall3,wall4]

    diaphragm1 = rigid_diaphragm(lateral_elements)

    diaphragm1.add_force_set("C1",[500,0,0],[0,0])

    diaphragm1.diapraghm_analysis_about_cor("C1")

    case = "C1"

    output = print_results(diaphragm1, lateral_elements, case)

    for line in output:
        print(line)