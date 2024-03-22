@echo off
echo Running Python script...
python create_database.py
if %errorlevel% neq 0 (
    echo Script execution failed.
) else (
    echo Script executed successfully.
)
