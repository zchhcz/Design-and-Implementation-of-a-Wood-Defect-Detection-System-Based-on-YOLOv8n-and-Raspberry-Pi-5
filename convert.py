#!/usr/bin/env python3
"""
YOLO Model Converter
Convert PyTorch model to ONNX format
"""
import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description='Convert YOLO model to ONNX format')
    parser.add_argument('--model', type=str, default='best.pt', help='Path to YOLO model file')
    parser.add_argument('--format', type=str, default='onnx', help='Export format (onnx, torchscript, etc.)')
    args = parser.parse_args()

    print(f"Loading model: {args.model}")
    model = YOLO(args.model)

    print(f"Exporting to {args.format} format...")
    model.export(format=args.format)
    print("Export completed!")

if __name__ == '__main__':
    main()
