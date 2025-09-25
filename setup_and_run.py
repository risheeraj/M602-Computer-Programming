import subprocess
import sys
import os

def check_and_install_packages():
    required_packages = {
        'streamlit': 'streamlit>=1.28.0',
        'plotly': 'plotly>=5.15.0', 
        'pandas': 'pandas>=1.5.0'
    }
    
    missing_packages = []
    
    for package, version_spec in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(version_spec)
    
    if missing_packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return True
        
        except subprocess.CalledProcessError:
            print("Error: Failed to install packages. Please run manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_weather_modules():
    required_files = [
        'config.py',
        'weather_api.py',
        'data_manager.py',
        'weather_app.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print("\nMake sure you have these files from your weather app:")
        for file in required_files:
            print(f"   • {file}")
        return False
    
    return True

def run_streamlit():
    if not os.path.exists('streamlit_app.py'):
        print("Error: streamlit_app.py not found!")
        print("Please save the Streamlit code as 'streamlit_app.py'")
        return False
    
    print("Starting Weather Dashboard...")
    print("Opening in browser at http://localhost:8501")
    print("Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    
    except KeyboardInterrupt:
        print("\nWeather Dashboard stopped")
        return True
    
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        return False

def main():
    if not check_and_install_packages():
        return
    
    if not check_weather_modules():
        return
    
    success = run_streamlit()
    
    if not success:
        print("\nTry running manually with: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()