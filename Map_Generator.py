import numpy as np
terrain_size = (15, 32)  # Size of the terrain grid
terrain_data = np.zeros(terrain_size, dtype=int)


# Generate Perlin noise
def perlin(x, y):
    xi = int(x) & 255
    yi = int(y) & 255
    xf = x - int(x)
    yf = y - int(y)
    u = fade(xf)
    v = fade(yf)

    aa = p[p[xi] + yi]
    ab = p[p[xi] + yi + 1]
    ba = p[p[xi + 1] + yi]
    bb = p[p[xi + 1] + yi + 1]

    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)

    return (lerp(x1, x2, v) + 1) / 2


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a, b, t):
    return (1 - t) * a + t * b


def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h == 12 or h == 14 else 0)
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)


# Permutation table
p = np.arange(512, dtype=int)
np.random.shuffle(p)
p = np.tile(p, 2)

# Generate Perlin noise-based terrain
for y in range(terrain_size[0]):
    for x in range(terrain_size[1]):
        noise_val = perlin(x * 0.1, y * 0.1)

        if noise_val > 0.3:
            terrain_data[y, x] = 4
        elif noise_val > -0.3:
            terrain_data[y, x] = 1
        elif noise_val > -0.6:
            terrain_data[y, x] = 2

# Convert numpy array to list of lists
terrain_list = terrain_data.tolist()

# Display the generated terrain data
for row in terrain_list:
    row_str = ''.join(str(cell) for cell in row)
    print(row_str)
