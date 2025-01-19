@REM pyinstaller --noconfirm --log-level=WARN \
@REM     --onefile --nowindow \
@REM     --add-data="README:." \
@REM     --add-data="image1.png:img" \
@REM     --add-binary="libfoo.so:lib" \
@REM     --hidden-import=secret1 \
@REM     --hidden-import=secret2 \
@REM     --upx-dir=/usr/local/share/ \
@REM     __main__.py


pyinstaller "connect4/__main__.py" --onefile --icon "connect4/assets/ico4.ico"