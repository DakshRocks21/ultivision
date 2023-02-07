from kivy.app import App
from kivy.uix.image import Image, CoreImage
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import io
import numpy as np
import matplotlib.pyplot as plt

# --- main ---
 
    
class MyPaintApp(App):
    def build(self):
        self.image = Image()
        Clock.schedule_interval(self.update_image, 0.25)
        return self.image
    def generate_texture(self):
        """Generate random numpy array, plot it, save it, and convert to Texture."""
        
        # numpy array
        arr = np.random.randint(0, 100, size=10, dtype=np.uint8)
        
        # plot
        plt.clf() # remove previous plot
        plt.plot(arr)
        
        # save in memory
        data = io.BytesIO()
        plt.savefig(data)
        
        data.seek(0)  # move to the beginning of file
        
        return CoreImage(data, ext='png').texture
    
    def update_image(self, dt):
        """Replace texture in existing image."""
        
        self.image.texture = self.generate_texture()

# run function every 0.25 s


if __name__ == '__main__':
    MyPaintApp().run()