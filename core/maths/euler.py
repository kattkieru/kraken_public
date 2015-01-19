"""Kraken - maths.euler module.

Classes:
Euler -- Euler rotation.
"""

import math
from kraken.core.kraken_system import KrakenSystem as KS
from math_object import MathObject
from mat33 import Mat33

rotationOrderStrToIntMapping = {
    'xyz': 0,
    'XYZ': 0,
    'yzx': 1,
    'YZX': 1,
    'zxy': 2,
    'ZXY': 2,
    'xzy': 3,
    'XZY': 3,
    'zyx': 4,
    'ZYX': 4,
    'yxz': 5,
    'YXZ': 5
}

rotationOrderIntToStrMapping = [
    'XYZ',
    'YZX',
    'ZXY',
    'XZY',
    'ZYX',
    'YXZ'
]

class Euler(MathObject):
    """Euler rotation object."""

    def __init__(self, x=None, y=None, z=None, ro=None):
        """Initialize values for x,y,z, and rotation order values."""

        super(Euler, self).__init__()

        if x is not None and not isinstance(x, (int, float)):
            raise TypeError("Euler: Invalid type for 'x' argument. Must be an int or float.")

        if y is not None and not isinstance(y, (int, float)):
            raise TypeError("Euler: Invalid type for 'y' argument. Must be an int or float.")

        if z is not None and not isinstance(z, (int, float)):
            raise TypeError("Euler: Invalid type for 'z' argument. Must be an int or float.")

        if ro is not None and not isinstance(ro, (int)):
            if isinstance(ro, basestring):
                ro = rotationOrderStrToIntMapping[ro]
            else:
                raise TypeError("Euler: Invalid type for 'ro' argument. Must be an int or a string.")

        if x is not None and self.getTypeName(x) == 'Euler':
            self.rtval = x
        else:
            self.rtval = KS.inst().rtVal('Euler')
            if x is not None and y is not None and z is not None:
                if ro is not None:
                    self.set(x=x, y=y, z=z, ro=ro)
                else:
                    self.set(x=x, y=y, z=z)



    def __str__(self):
        """String representation of Euler object."""

        return "Euler(x=" + str(self.x) + ", y=" + str(self.y) + ", z=" + str(self.z) + ", ro= '" + str(self.ro) + "')"


    @property
    def x(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.x


    @x.setter
    def x(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.x = KS.inst().rtVal('Scalar', value)


    @property
    def y(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.y


    @y.setter
    def y(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.y = KS.inst().rtVal('Scalar', value)


    @property
    def z(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return self.rtval.z


    @z.setter
    def z(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        self.rtval.z = KS.inst().rtVal('Scalar', value)


    @property
    def ro(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        return rotationOrderIntToStrMapping[self.rtval.ro.order]


    @ro.setter
    def ro(self, value):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """
        self.rtval.ro.order = KS.inst().rtVal('Integer', value)


    def clone(self):
        """Returns a clone of the Euler.

        Return:
        The cloned Euler

        """

        euler = Euler();
        euler.x = self.x;
        euler.y = self.y;
        euler.z = self.z;
        euler.ro = self.ro;

        return euler


    # Setter from scalar components
    def set(self, x, y, z, ro=None):
        """Doc String.

        Arguments:
            x, y, z -- Scalar, the angles in radians to set the eulaer angles to.
            ro -- Integer, the rotation order to use in the euler angles.

        Return:
        True if successful.

        """
        self.rtval.set('', KS.inst().rtVal('Scalar', x), KS.inst().rtVal('Scalar', y), KS.inst().rtVal('Scalar', z))
        if ro is not None:
            if isinstance(ro, basestring):
                ro = rotationOrderStrToIntMapping[ro]
            self.rtval.ro.order = KS.inst().rtVal('Integer', ro)



    def equal(self, other):
        """Checks equality of this Euler with another.

        Arguments:
        other -- Euler, other value to check equality with.

        Return:
        True if equal.

        """

        return self.rtval.equal('Boolean', KS.inst().rtVal('Euler', other))


    def almostEqual(self, other, precision):
        """Checks almost equality of this Euler with another.

        Arguments:
        other -- Euler, other value to check equality with.
        precision -- Scalar, precision value.

        Return:
        True if almost equal.

        """

        return self.rtval.almostEqual('Boolean', KS.inst().rtVal('Euler', other), KS.inst().rtVal('Scalar', precision))


    def toMat33(self):
        """Converts the Euler angles value to a Mat33.

        Return:
        The Mat33 value

        """

        return Mat33(self.rtval.toMat33('Mat33'))


