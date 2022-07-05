# UAV-Mapping-Missions-for-Litchi-QGIS-Plugin
Copy the entire 'drone_path' folder to C:/Users/COMPUTER_NAME/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins - Let the QGIS Application be closed when you do this.
Once the folder is copied, open QGIS 3.x
Open 'Manage and Install Plugins' and tick 'Drone_path'.
Go to Vectors and click on Drone Path --> Draw Grid Lines.
Some default values of Drone and Camera parameters appear which can be changed. 
Use an appropriate polygon as AOI. 
An input line is required to which parallel lines will be drawn. There is an input in the plugin 'No. of parallel line' - enter the number of lines that must be drawn parallel to the input line to cover the entire AOI. Parallel lines are drawn to the right of input line.
Fill the appropriate values and calculate. Output is a csv file with lat lon values and other columns necessary for FlyLitchi.
