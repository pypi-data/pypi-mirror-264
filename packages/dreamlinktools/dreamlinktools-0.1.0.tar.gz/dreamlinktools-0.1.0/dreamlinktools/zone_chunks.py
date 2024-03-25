from os.path import join, exists, dirname
from os import makedirs
from json import loads
from dreamtools.utils.vec3 import Vec3
from dreamtools.config import chunk_dims

class ZoneChunks:
    def __init__(self, directory):
        self.directory = directory
        zone_config_path = join(self.directory, "zone.json")
        with open(zone_config_path, "r") as f:
            zone = loads(f.read())
        x, y, z = zone["terrain.dimensions.chunk_space"]
        self.chunk_space_dimensions = Vec3(x, y, z)
        self.block_space_dimensions = self.chunk_space_dimensions * chunk_dims
        self.chunk_data = bytearray(self.block_space_dimensions.volume())

    def load(self):
        chunks_path = join(self.directory, ".gen/chunks.dat") 
        if exists(chunks_path):
            with open(chunks_path, "rb") as f:
                f.readinto(self.chunk_data)

    def save(self):
        chunks_path = join(self.directory, ".gen/chunks.dat") 
        makedirs(dirname(chunks_path), exist_ok=True)
        with open(chunks_path, "wb") as f:
            f.write(self.chunk_data)

    def get_index(self, position):
        chunk_space_position = position // chunk_dims
        chunk_ix = chunk_space_position.pack(self.chunk_space_dimensions)
        chunk_block_space_position = position % chunk_dims
        block_ix = chunk_block_space_position.pack(chunk_dims)
        return chunk_ix * chunk_dims.volume() + block_ix

    def __getitem__(self, x, y, z):
        data_ix = self.get_index(Vec3(x, y, z))
        return self.chunk_data[data_ix]

    def __setitem__(self, x, y, z, value):
        data_ix = self.get_index(Vec3(x, y, z))
        self.chunk_data[data_ix] = value

