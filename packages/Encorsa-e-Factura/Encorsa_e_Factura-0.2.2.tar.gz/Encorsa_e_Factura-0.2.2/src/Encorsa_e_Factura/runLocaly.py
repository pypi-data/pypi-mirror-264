import socket
import sincronizare
import sincronizare

print(socket.gethostname())

device_name = socket.gethostname()
if(device_name == 'LAPTOP-B8RMJEVP'):
    sincronizare.startRunning(r'C:\Cod\e-Factura-PythonLibrary\DEV\parameters.json', r'C:\Cod\e-Factura-PythonLibrary\DEV\xmlTemplate.xml')
if(device_name == 'DESKTOP-NF89BJF'):
    sincronizare.startRunning(r'D:\ENCORSA\e-Factura-V2\e-Factura-PythonLibrary\DEV\parameters.json', r'D:\ENCORSA\e-Factura-V2\e-Factura-PythonLibrary\DEV\xmlTemplate.xml')
