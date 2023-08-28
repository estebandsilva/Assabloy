import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

class TemperatureColormapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Temperature Colormap")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.img_item = pg.ImageItem()
        self.plot_widget.addItem(self.img_item)

        self.x_range = 50
        self.y_range = 50
        self.temperature_data = np.zeros((self.y_range, self.x_range))

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_colormap)
        self.timer.start(1000)  # Update every 1 second

    def update_colormap(self):
        x = np.arange(self.x_range)
        y = np.arange(self.y_range)
        xx, yy = np.meshgrid(x, y)

        new_temperature = self.generate_random_temperature()
        self.temperature_data = np.roll(self.temperature_data, -1, axis=0)
        self.temperature_data[-1, :] = new_temperature

        # Interpolate and create a larger grid
        larger_grid_x, larger_grid_y = np.meshgrid(np.linspace(0, self.x_range - 1, 500),
                                                    np.linspace(0, self.y_range - 1, 500))
        interpolated_temperature = griddata((xx.ravel(), yy.ravel()), self.temperature_data.ravel(),
                                            (larger_grid_x, larger_grid_y), method='cubic')

        # Apply Gaussian filter
        interpolated_temperature = gaussian_filter(interpolated_temperature, sigma=1.0)
        self.img_item.setImage(interpolated_temperature, autoLevels=True, lut=self.get_colormap())

    def generate_random_temperature(self):
        return np.random.uniform(20, 30, size=self.x_range)



    def get_colormap(self):
        colors = [
            (0, 0, 255, 255),  # Blue
            (0, 255, 255, 255),  # Cyan
            (0, 255, 0, 255),  # Green
            (255, 255, 0, 255),  # Yellow
            (255, 0, 0, 255)  # Red
        ]
        positions = [0.0, 0.25, 0.5, 0.75, 1.0]  # Corresponding positions for colors
        colormap = pg.ColorMap(pos=positions, color=colors)
        return colormap.getLookupTable(nPts=256, alpha=False)

def main():
    app = QApplication(sys.argv)
    window = TemperatureColormapApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
