run:
	python3 -m forecast

# Target to create a bundled single executable using PyInstaller
bundle:
	pyinstaller --clean --dist ./dist/linux forecast.spec

# Target to create a portable MS Windows executable using cx_Freeze inside Docker
bundle-windows:
	docker run --rm -v $(PWD):/src -w /src --user $(id -u):$(id -g) cdrx/pyinstaller-windows:python3 \
	"python setup.py build_exe --build-exe ./dist/windows"

# Target to run the generated Windows executable via Docker
run-wine:
	xhost +local:
	docker run --rm -e DISPLAY=:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/dist:/src/dist -w /src --user $(id -u):$(id -g) cdrx/pyinstaller-windows:python3 \
		"wine dist/windows/forecast.exe"
