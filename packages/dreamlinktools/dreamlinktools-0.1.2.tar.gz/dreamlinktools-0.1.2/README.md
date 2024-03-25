# dreamlink-tools

## Installation

```
pip install dreamlinktools
```

## Usage

```
from dreamlinktools.zone_chunks import ZoneChunks
from dreamlinktools.utils.vec3 import Vec3

zone_chunks = ZoneChunks("<level_path>")
zone_chunks.load()
zone_chunks[Vec3(1,2,1)] = 5 # block ID
zone_chunks.save()
```
