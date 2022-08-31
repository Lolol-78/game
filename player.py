from ursina import *
from direct.actor.Actor import Actor



class Player(Entity):
    
    def __init__(self):
        super().__init__()
        self.actor = Actor("assets/perso/perso.gltf")
        self.actor.reparent_to(self)
        self.actor.loop("Attacking_Idle")
        self.animation=["Run", 
                        "Walk", 
                        "Idle", # don't work
                        "Roll", 
                        "RecieveHit_Attacking", 
                        "RecieveHit", # don't work
                        "Punch", # don't work
                        "PickUp", # don't work'
                        "Death", 
                        "Dagger_Attack", 
                        "Dagger_Attack2", 
                        "Attacking_Idle"]
        self.control="zqsd"
        self.speed_control = "left shift"
        self.mouse_sensitivity = Vec2(40, 40)
        
        self.camera_height = 2.3
        self.camera_view = [[Vec3(0, 9, 15), 180], 
                            [Vec3(0, 0, -10), 0]]
        self.camera_view_number = 0
        
        self.speed = 0.08
        self.running_multiplier = 1
        
        # self.truc = Entity(model="cube", color=color.red)
        # self.truc.parent = self
        # self.truc.rotation_x=3.448276 * (self.camera_view[self.camera_view_number][0][1] - 2.3)
        # self.truc.rotation_y=self.camera_view[self.camera_view_number][1]
        # self.truc.position=self.camera_view[self.camera_view_number][0]
        
        camera.parent = self
        camera.rotation_x=3.448276 * self.camera_view[self.camera_view_number][0][1]
        camera.rotation_y=self.camera_view[self.camera_view_number][1]
        camera.position=self.camera_view[self.camera_view_number][0]
    
    
    def is_moving(self):
        for i in range(4):
            if held_keys[self.control[i]]:
                return True
        return False
    
    def is_running(self):
        if held_keys[self.speed_control]:
            return True
        else:
            return False
    
    def update(self):
        
        
        
        # change the players rotation if the mouse move
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        
        
        
        # move the player if keys are pressed
        if held_keys[self.control[0]]:
            self.position+=self.back*self.speed*self.running_multiplier
        if held_keys[self.control[1]]:
            self.position+=self.right*self.speed*self.running_multiplier
        if held_keys[self.control[2]]:
            self.position+=self.forward*self.speed*self.running_multiplier
        if held_keys[self.control[3]]:
            self.position+=self.left*self.speed*self.running_multiplier
        
        
        
        # animate the player
        if self.is_moving():
            if self.is_running():
                self.running_multiplier = 2
                if self.actor.getCurrentFrame() >= 19:
                    self.actor.loop(self.animation[0])
                else:
                    self.actor.loop(self.animation[0], restart=0)
            else:
                self.running_multiplier = 1
                if self.actor.getCurrentFrame() >= 29:
                    self.actor.loop(self.animation[1])
                else:
                    self.actor.loop(self.animation[1], restart=0)
        
        else:
            if self.actor.getCurrentFrame() >= 39:
                self.actor.loop(self.animation[-1])
            else:
                self.actor.loop(self.animation[-1], restart=0)
        
        
        
        
        
        
        
        
        
        # make sure the player is on the ground
        y_ray=raycast((self.x, self.y+self.scale_y*2.63/2, self.z), direction=(0, -1, 0), ignore=[self])
                
        if y_ray.distance != math.inf:
            self.y+=self.scale_y*2.63/2
            self.y-=y_ray.distance
        
        
        
        # move the camera closer to the player if there is an object between them
        distance=sqrt(self.camera_view[self.camera_view_number][0][1]**2 + self.camera_view[self.camera_view_number][0][2]**2)
        
        camera_player_ray = raycast(origin = (self.x, self.y+self.camera_height, self.z), 
                                    direction = self.back * (2 * self.camera_view_number - 1) + Vec3(0, (2/30) * self.camera_view[self.camera_view_number][0][1], 0),
                                    distance = distance, 
                                    ignore = [self])
        
        if camera_player_ray.hit:
            
            camera.y = self.camera_view[self.camera_view_number][0][1] * camera_player_ray.distance / distance + self.camera_height
            camera.z = self.camera_view[self.camera_view_number][0][2] * camera_player_ray.distance / distance
        else:
            camera.position = self.camera_view[self.camera_view_number][0] + Vec3(0, self.camera_height, 0)
        