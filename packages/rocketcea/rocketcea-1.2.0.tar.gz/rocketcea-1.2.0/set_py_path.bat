
rem set python path variable (Default is Python 3.10 64 bit)
IF "%1"=="" ( SET "MYPYTHONPATH=C:\Python310" ) ELSE ( SET "MYPYTHONPATH=D:\py_versions\Python%1_64" )

rem Make sure that PATH is as simple as possible
set PATH=C:\MinGW\mingw64\bin;C:\MinGW\mingw64\lib;%MYPYTHONPATH%;%MYPYTHONPATH%\Scripts

