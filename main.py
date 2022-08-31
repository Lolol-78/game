from ursina import *
from ursina.shaders import lit_with_shadows_shader
from player import Player
import random

app = Ursina(size=(1000, 800))

random_generator=random.Random()

mouse.locked=True
# EditorCamera()


Sky()

player=Player()

ground = Entity(model="assets/map/plane/plane", texture="assets/map/plane/plane_texture", collider="mesh", shader=lit_with_shadows_shader)

grass_patch=[]

for i in range(10):
    for j in range(10):
        grass_patch.append(Entity(model="assets/map/grass/grass", x=19-i, z=19-j, y=1.7, rotation_y=random_generator.randint(0, 90), texture="assets/map/grass/grass_texture", double_sided=True))

tree = Entity(model="assets/map/tree/tree", position=(-9.5, 2.2, -3.5), shader=lit_with_shadows_shader)


tree_hitbox=[Entity(model="cube", position=(-9.5, 4.2, -3.5), scale=(0.5, 4, 0.5), collider="mesh", visible=False),
            Entity(model="cube", position=(-9.4, 7, -3.5), scale=(4, 4, 3), collider="mesh", visible=False)]

def input(key):
        
        if key == 'space':
            
            player.camera_view_number += 1
            player.camera_view_number %= len(player.camera_view)
            camera.rotation_y = player.camera_view[player.camera_view_number][1]
            camera.rotation_x = 3.448276 * player.camera_view[player.camera_view_number][0][1]
    




DirectionalLight()
AmbientLight()

app.run()