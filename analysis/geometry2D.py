class Node2D():
    '''
    class reprsenting the nodes of the structure in 2D x,y plane or R2
    '''

    def __init__(self, x, y, userid, number):
        '''
        x: float        x-coordinate of node
        y: float        y-cootdinate of node
        userid: string  User assigned name for the node
        number: int     User/Program assigned node number
        '''

        # Location in space
        self.x = x
        self.y = y

        # Indetifiers
        self.userid = userid
        self.number = number

        # Support condition initialized to all released
        # [Fx, Fy, Mz] or [tx,ty,rz]
        self.support = [0, 0, 0]

    def __str__(self):
        '''
        define what will display when print() is called on a node object
        '''
        print(f'Node: {self.userid}')
        print(f'Node #: {self.number}')
        print(f'x: {self.x:4f}')
        print(f'y: {self.y:4f}')
        return f'Restraint: {self.support}'

    def supports(self, restraints):
        '''
        update the support conditions

        restraints: [int,int,int]   restraint condition
                                    1 = restrained
                                    0 = unrestrained
                    [tx,ty,rz]
        '''

        self.support = restraints
