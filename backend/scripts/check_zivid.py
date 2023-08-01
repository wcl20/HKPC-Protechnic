import zivid

if __name__ == '__main__':

    app = zivid.Application()
    camera = app.connect_camera()
    settings = zivid.Settings(acquisitions=[zivid.Settings.Acquisition()])
    frame = camera.capture(settings)
    xyz = frame.point_cloud().copy_data("xyz") # Get point coordinates as [Height,Width,3] float array
    rgba = frame.point_cloud().copy_data("rgba") # Get point colors as [Height,Width,4] uint8 array
