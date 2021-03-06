import math
from random import Random

class Quaternion(object):

    def get_random_quaternion(random = Random()):
        """
        Gets a random unit Quaternion.

        Rotations generated by Quaternions produced by this method are NOT gauranteed to be randomly distributed.

        Args:
            random - the random object used to generate this quaternion. Default is a new Random with a random seed.

        Returns:
            a new random normalized Quaternion.
        """

        return Quaternion(0.5 - random.random(), 0.5 - random.random(), 0.5 - random.random(), 0.5 - random.random()).normalized()

    def get_random_rotation_quaternion(random = Random()):
        """
        Gets a random unit Quaternion such that the rotation created by this unit Quaternion is just as likely as any other rotation

        Args:
            random - the random object used to generate this quaternion. Default is a new Random with a random seed.

        Returns:
            a new evenly distributed unit rotation Quaternion
        """

        # first generate a random unit vector
        # horizontal rotation of unit vector
        theta = math.pi - random.random() * 2 * math.pi
        # vertical rotation of unit vector
        phi = math.asin(random.random()) * (-1 if random.random() < 0.5 else 1)

        # rotation around unit vector
        rotation = math.pi - random.random() * 2 * math.pi

        # now create the Quaternion of rotation
        return Quaternion(math.cos(rotation/2), math.sin(rotation/2) * math.sin(phi) * math.cos(theta), math.sin(rotation/2) * math.sin(phi) * math.sin(theta), math.sin(rotation/2) * math.cos(phi))
    
    def __init__(self, r, i, j, k):
        """
        Creates a new Quaternion from the given real component (r) and 3 imaginary components (i, j, k)

        Args:
            r   - the real component
            i   - the first imaginary component
            k   - the second imaginary component
            j   - the third imaginary component

        Returns:
            a new Quaternion
        """

        self.r = r
        self.i = i
        self.j = j
        self.k = k

    def __add__(self, other):
        """
        Defines addition of Quaternions as adding each of their components

        Args:
            other - the other Quaternion to add to this one

        Returns:
            the sum of the two Quaternions as a new Quaternion with components equal to the sum of the components in this Quaternion and the other
        """

        return Quaternion(self.r + other.r, self.i + other.i, self.j + other.j, self.k + other.k)

    def __sub__(self, other):
        """
        Defines subtraction of Quaternions as subtracting each of their components

        Args:
            other - the other Quaternion to subtract from this one

        Returns:
            the difference of two Quaternions as a new Quaternion with components equal to that of this Quaternion minus those of the other Quaternion
        """
        return Quaternion(self.r - other.r, self.i - other.i, self.j - other.j, self.k - other.k)

    def __mul__(self, other):
        """
        Defines the product of Quaternions as *magic*

        Note: multiplication of Quaternions is non-commutative

        Args:
            other - the other Quaternion to multiply with this one

        Returns:
            a new Quaternion that is the product of this one and the other
        """

        return Quaternion(
            self.r * other.r - self.i * other.i - self.j * other.j - self.k * other.k,
            self.r * other.i + self.i * other.r + self.j * other.k - self.k * other.j,
            self.r * other.j - self.i * other.k + self.j * other.r + self.k * other.i,
            self.r * other.k + self.i * other.j - self.j * other.i + self.k * other.r
        )

    def __abs__(self):
        """
        Defines the absolute value of a Quaternion as its length

        Args:
            None

        Returns:
            the length of this Quaternion
        """

        return math.sqrt(self.r ** 2 + self.i ** 2 + self.j ** 2 + self.k ** 2)

    def __neg__(self):
        """
        Defines the negation of a Quaternion as the negation of each of its components

        Args:
            None

        Returns:
            a new Quaternion with components equal to the negated components of this Quaternion
        """

        return Quaternion(-self.r, -self.i, -self.j, -self.k)

    def __pos__(self):
        """
        Defines the posation of a Quaternion as a clone

        Args:
            None

        Returns:
            a new Quaternion with components identical to this Quaternion
        """
        return Quaternion(+self.r, +self.i, +self.j, +self.k)

    def __eq__(self, other):
        """
        Defines Quaternion equivelence as equivelence of all components

        Args:
            other - the Quaternion to compare to this one

        Returns:
            True if these Quaternions have identical components, False otherwise
        """

        return self.r == other.r and self.i == other.i and self.j == other.j and self.k == other.k

    def __ne__(self, other):
        """
        Defines Quaternion non-equivelence as non-equivelence of any components

        Args:
            other - the Quaternion to compare to this one

        Returns:
            True if these Quaternions are have any different components
        """

        return self.r != other.r or self.i != other.i or self.j != other.j or self.k != other.k

    def normalized(self):
        """
        Creates a new unit Quaternion by normalizing this one

        Args:
            None

        Returns:
            A new Quaternion that is the normalized version of this one
        """

        length = abs(self)
        return Quaternion(self.r / length, self.i / length, self.j / length, self.k / length)

    def conjugate(self):
        """
        Creates a new Quaternion that is the complex conjugate of this one

        The product of a Quaternion and its conjugate is a real number (i, j, k are all 0)

        Args:
            None

        Returns:
            this Quaternion's conjuage
        """

        return Quaternion(self.r, -self.i, -self.j, -self.k)

    def rotate(self, x, y, z, origin_x = 0, origin_y = 0, origin_z = 0):
        """
        Rotates a point in space by the rotation defined by this Quaternion

        Args:
            x - the x of the point to rotate
            y - the y of the point to rotate
            z - the z of the point to rotate
            origin_x - the x of the point to rotate about
            origin_y - the y of the point to rotate about
            origin_z - the z of the point to rotate about

        Returns:
            x, y, z as defined by the input rotated by this Quaternion
        """

        vector_quaternion = Quaternion(0, x - origin_x, y - origin_y, z - origin_z)

        rotated_quaternion = self * vector_quaternion * self.conjugate()

        x = rotated_quaternion.i + origin_x
        y = rotated_quaternion.j + origin_y
        z = rotated_quaternion.k + origin_z

        return x, y, z
