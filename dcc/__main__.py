"""Main entry point for dive color correction."""

import argparse
import sys
from .core.correction import correct_image, analyze_video

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Dive Color Corrector")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI interface")
    parser.add_argument("input", nargs="?", help="Input file or directory")
    parser.add_argument("output", nargs="?", help="Output file or directory")
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    if args.gui:
        try:
            from .gui.app import run_gui
            run_gui()
        except ImportError:
            print("Error: GUI dependencies not installed. Install with: pip install 'dcc[gui]'")
            sys.exit(1)
        return
    
    if not args.input or not args.output:
        print("Error: Input and output paths are required in CLI mode")
        sys.exit(1)
        
    # Process files based on type
    if args.input.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
        analyze_video(args.input, args.output)
    else:
        correct_image(args.input, args.output)

if __name__ == "__main__":
    main() 