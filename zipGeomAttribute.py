"""

Contains the methods for zipping the resources needed for a functioning plugin

"""

import zipfile
import os

def zipGeomAttribute():
    """Zips the files needed for the plugin to be installed into QGIS"""
    print('creating archive')
    zipWrite = zipfile.ZipFile('geomAttribute.zip', mode='w')

    #what files do I need for QT window to work?

    fileList = ['geomAttribute.py','parseQGISGeometry.py', '__init__.py', 'geomAttribute_window.py',
            'modelVectorLayers.py', 'metadata.txt', 'resources.py', 'geomAttribute_window_base.ui']
    folderList = ['icons']
    try:
        print('Adding files')
        for item in fileList:
            zipWrite.write(item, 'geomAttribute/' + item)

        for folder in folderList:
            for file in os.listdir(os.path.join(os.path.dirname(__file__), folder)):
                file = folder + '/' + file
                zipWrite.write(file, 'geomAttribute/' + file)

    finally:
        print('closing')
        #zipWrite.close()

def installGeomAttributeFromZip():
    """Unzips the zipped folder.  An automation used for testing."""
    zipRead = zipfile.ZipFile('geomAttribute.zip', mode='r')
    zipRead.extractall('C:/Users/pippi/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/')
    zipRead.close()


if __name__ == '__main__':
    zipGeomAttribute()
    installGeomAttributeFromZip()