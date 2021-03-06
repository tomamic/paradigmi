set MODULE=knightdom

set SWIG_HOME=%TMP%\swigwin-3.0.12
set PYTHON_HOME=%LOCALAPPDATA%\Programs\Python\Python36-32
set MINGW_HOME=%PROGRAMFILES(X86)%\CodeBlocks\MinGW

set PATH=%MINGW_HOME%\bin;%SWIG_HOME%;%PATH%
swig -python -c++ %MODULE%.i
g++ -std=c++11 -D_hypot=hypot -c %MODULE%.cpp %MODULE%_wrap.cxx -I"%PYTHON_HOME%\include"
g++ -shared *.o "%PYTHON_HOME%\libs\libpython36.a" -o _%MODULE%.pyd

pause
