# How to run

## Clone project
Clone the project into a suitable folder.

## Install Python
Install Python version 3.11.0

## Install requiered libraries
```
pip install -r requirements.txt
```
`pybullet` may require some additional installations.

## Fix project-path
In the file `assets/config/config.json`, set desired `project_path`.

In your project folder, add the folder `AttackerTestProject`

## How to start the program
Run all commands in the top level of the folder. Current functionality allows the user to start the provided example project and run it. You do however need to move the dearpygui windows out of the way as they appear on top of eachother. This can be done within the window that appears when running the main file.
```
python /src/main.py
```
