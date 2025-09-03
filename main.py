# main.py - Entry point for Travel Assistant application
import sys
import os

def main():
    """Main entry point with mode selection"""
    print("Travel Assistant")
    print("=" * 30)
    print("Choose your mode:")
    print("1. Interactive CLI (chat with the assistant)")
    print("2. Run test suite (batch testing)")
    print("3. Web Interface (Streamlit app)")
    print("4. Exit")
    print("-" * 30)
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\nStarting CLI mode...")
                from cli import main as cli_main
                cli_main()
                break
                
            elif choice == "2":
                print("\nStarting test suite...")
                from test_run import run_test_suite
                run_test_suite()
                break
                
            elif choice == "3":
                print("\nStarting web interface...")
                print("The Streamlit app will open in your default web browser.")
                print("If it doesn't open automatically, go to: http://localhost:8501")
                print("Press Ctrl+C to stop the web server.")
                try:
                    import subprocess
                    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
                except subprocess.CalledProcessError:
                    print("Error: Could not start Streamlit. Make sure it's installed: pip install streamlit")
                except KeyboardInterrupt:
                    print("\nWeb interface stopped.")
                break
                
            elif choice == "4":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
