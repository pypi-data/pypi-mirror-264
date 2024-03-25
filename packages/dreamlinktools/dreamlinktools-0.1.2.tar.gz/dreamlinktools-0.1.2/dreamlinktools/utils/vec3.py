class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __floordiv__(self, other):
        return Vec3(self.x // other.x, self.y // other.y, self.z // other.z)

    def __mod__(self, other):
        return Vec3(self.x % other.x, self.y % other.y, self.z % other.z)

    def volume(self):
        return self.x * self.y * self.z

    def pack(self, dims):
        index = 0
        index += self.y * dims.z * dims.x
        index += self.z * dims.x
        index += self.x
        return index
        
    @staticmethod
    def unpack(value, dims):
        x = value % dims.x
        value //= dims.x
        z = value % dims.z
        value //= dims.z
        y = value
        return Vec3(x, y, z)

