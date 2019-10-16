from setuptools import setup

setup(name='isPLC-modbus',
      version='1.0',
      description='一個isPLC的通訊模組(modbus版)',
      url='https://github.com/InterfaceGUI/pyisPLC-modbus.git',
      author='LarsHagrid',
      author_email='interfacegui@gmail.com',
      license='GNU Lesser General Public License v3.0',
      packages=['isPLC'],
      install_requires=[
          'crcmod>=1.7',
          'pyserial>=3.4'
      ],
      zip_safe=False)

