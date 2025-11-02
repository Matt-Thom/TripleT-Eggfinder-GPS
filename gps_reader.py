#!/usr/bin/env python3
# /mnt/GAMES_SSD/matt/Code/TripleT-Eggfinder-GPS-Test/gps_reader.py
# Reads GPS data from USB serial module and displays parsed information
# Created to parse NMEA sentences from Eggfinder GPS module connected via /dev/ttyUSB0
# RELEVANT FILES: README.md, AI_Rules.md

import serial
import sys
from datetime import datetime

def parse_gps_coordinates(coord_str, direction):
    """
    Parse GPS coordinate string into decimal degrees.
    
    Args:
        coord_str: Coordinate string in DDMM.MMMM or DDDMM.MMMM format
        direction: Direction indicator (N/S/E/W)
    
    Returns:
        float: Coordinate in decimal degrees, or None if invalid
    """
    if not coord_str or not direction:
        return None
    
    try:
        # For latitude: DDMM.MMMM (first 2 digits are degrees)
        # For longitude: DDDMM.MMMM (first 3 digits are degrees)
        if direction in ['N', 'S']:
            degrees = float(coord_str[:2])
            minutes = float(coord_str[2:])
        else:  # E or W
            degrees = float(coord_str[:3])
            minutes = float(coord_str[3:])
        
        # Convert to decimal degrees
        decimal = degrees + (minutes / 60.0)
        
        # Apply direction (South and West are negative)
        if direction in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    except (ValueError, IndexError):
        return None

def parse_nmea_sentence(sentence):
    """
    Parse a single NMEA sentence and extract relevant GPS data.
    
    Args:
        sentence: Raw NMEA sentence string
    
    Returns:
        dict: Parsed GPS data or None if sentence is invalid/unsupported
    """
    # Remove any whitespace and check for valid NMEA sentence
    sentence = sentence.strip()
    if not sentence.startswith('$') or '*' not in sentence:
        return None
    
    # Split sentence into data and checksum
    try:
        data_part, checksum = sentence.split('*')
        fields = data_part.split(',')
        sentence_type = fields[0]
    except ValueError:
        return None
    
    # Parse GPGGA sentence (Global Positioning System Fix Data)
    # This contains position, altitude, and fix quality information
    if sentence_type in ['$GPGGA', '$GNGGA']:
        try:
            return {
                'type': 'GPGGA',
                'time': fields[1] if len(fields) > 1 else None,
                'latitude': parse_gps_coordinates(fields[2], fields[3]) if len(fields) > 3 else None,
                'longitude': parse_gps_coordinates(fields[4], fields[5]) if len(fields) > 5 else None,
                'fix_quality': int(fields[6]) if len(fields) > 6 and fields[6] else 0,
                'satellites': int(fields[7]) if len(fields) > 7 and fields[7] else 0,
                'altitude': float(fields[9]) if len(fields) > 9 and fields[9] else None,
                'altitude_units': fields[10] if len(fields) > 10 else None
            }
        except (ValueError, IndexError):
            return None
    
    # Parse GPRMC sentence (Recommended Minimum Specific GPS/Transit Data)
    # This contains position, speed, and course information
    elif sentence_type in ['$GPRMC', '$GNRMC']:
        try:
            return {
                'type': 'GPRMC',
                'time': fields[1] if len(fields) > 1 else None,
                'status': fields[2] if len(fields) > 2 else None,  # A=active, V=void
                'latitude': parse_gps_coordinates(fields[3], fields[4]) if len(fields) > 4 else None,
                'longitude': parse_gps_coordinates(fields[5], fields[6]) if len(fields) > 6 else None,
                'speed_knots': float(fields[7]) if len(fields) > 7 and fields[7] else None,
                'course': float(fields[8]) if len(fields) > 8 and fields[8] else None,
                'date': fields[9] if len(fields) > 9 else None
            }
        except (ValueError, IndexError):
            return None
    
    return None

def format_gps_time(time_str):
    """
    Format GPS time string (HHMMSS.sss) into readable format.
    
    Args:
        time_str: Time string from GPS in HHMMSS.sss format
    
    Returns:
        str: Formatted time string or 'N/A' if invalid
    """
    if not time_str or len(time_str) < 6:
        return 'N/A'
    
    try:
        hours = time_str[0:2]
        minutes = time_str[2:4]
        seconds = time_str[4:6]
        return f"{hours}:{minutes}:{seconds} UTC"
    except (ValueError, IndexError):
        return 'N/A'

def display_gps_data(gga_data=None, rmc_data=None):
    """
    Display parsed GPS data in a clean, structured format.
    
    Args:
        gga_data: Parsed GPGGA sentence data (position and altitude)
        rmc_data: Parsed GPRMC sentence data (speed and course)
    """
    # Clear screen for clean display (works on Linux/Mac)
    print('\033[2J\033[H', end='')
    
    print("=" * 60)
    print("GPS DATA DISPLAY".center(60))
    print("=" * 60)
    print()
    
    # Display timestamp
    print(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Display position data (from GPGGA or GPRMC)
    print("POSITION DATA")
    print("-" * 60)
    
    if gga_data:
        print(f"GPS Time:    {format_gps_time(gga_data.get('time'))}")
        
        lat = gga_data.get('latitude')
        lon = gga_data.get('longitude')
        
        if lat is not None and lon is not None:
            print(f"Latitude:    {lat:.6f}°")
            print(f"Longitude:   {lon:.6f}°")
        else:
            print("Latitude:    N/A")
            print("Longitude:   N/A")
        
        # Display fix quality
        fix_quality = gga_data.get('fix_quality', 0)
        fix_status = {
            0: "No Fix",
            1: "GPS Fix",
            2: "DGPS Fix",
            3: "PPS Fix",
            4: "RTK Fix",
            5: "Float RTK",
            6: "Estimated"
        }
        print(f"Fix Quality: {fix_status.get(fix_quality, 'Unknown')} ({fix_quality})")
        print(f"Satellites:  {gga_data.get('satellites', 0)}")
        
        # Display altitude
        alt = gga_data.get('altitude')
        if alt is not None:
            print(f"Altitude:    {alt:.1f} {gga_data.get('altitude_units', 'M')}")
        else:
            print("Altitude:    N/A")
    
    elif rmc_data:
        print(f"GPS Time:    {format_gps_time(rmc_data.get('time'))}")
        
        lat = rmc_data.get('latitude')
        lon = rmc_data.get('longitude')
        
        if lat is not None and lon is not None:
            print(f"Latitude:    {lat:.6f}°")
            print(f"Longitude:   {lon:.6f}°")
        else:
            print("Latitude:    N/A")
            print("Longitude:   N/A")
        
        status = rmc_data.get('status')
        print(f"Status:      {'Active' if status == 'A' else 'Void/Invalid'}")
    else:
        print("Waiting for GPS data...")
    
    print()
    
    # Display movement data (from GPRMC)
    if rmc_data:
        print("MOVEMENT DATA")
        print("-" * 60)
        
        speed_knots = rmc_data.get('speed_knots')
        if speed_knots is not None:
            speed_kmh = speed_knots * 1.852  # Convert knots to km/h
            speed_mph = speed_knots * 1.15078  # Convert knots to mph
            print(f"Speed:       {speed_knots:.2f} knots ({speed_kmh:.2f} km/h, {speed_mph:.2f} mph)")
        else:
            print("Speed:       N/A")
        
        course = rmc_data.get('course')
        if course is not None:
            print(f"Course:      {course:.1f}°")
        else:
            print("Course:      N/A")
        
        print()
    
    print("=" * 60)
    print("Press Ctrl+C to exit")
    print()

def main():
    """
    Main function to connect to GPS module and continuously read/display data.
    """
    port = '/dev/ttyUSB0'
    baudrate = 9600
    
    print(f"Connecting to GPS module on {port} at {baudrate} bps...")
    
    try:
        # Open serial connection to GPS module
        # Timeout is set to 1 second to prevent blocking indefinitely
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected successfully!")
        print("Reading GPS data...\n")
        
        # Store the most recent parsed data from each sentence type
        # This allows us to combine data from multiple sentence types
        latest_gga = None
        latest_rmc = None
        
        while True:
            try:
                # Read one line from the serial port
                # GPS modules typically send one NMEA sentence per line
                line = ser.readline().decode('ascii', errors='ignore')
                
                if line:
                    # Parse the NMEA sentence
                    parsed = parse_nmea_sentence(line)
                    
                    if parsed:
                        # Update our stored data based on sentence type
                        if parsed['type'] == 'GPGGA':
                            latest_gga = parsed
                            # Display immediately when we get position fix data
                            display_gps_data(gga_data=latest_gga, rmc_data=latest_rmc)
                        
                        elif parsed['type'] == 'GPRMC':
                            latest_rmc = parsed
                            # Display with combined data
                            display_gps_data(gga_data=latest_gga, rmc_data=latest_rmc)
            
            except UnicodeDecodeError:
                # Sometimes serial data can be corrupted, just skip it
                continue
    
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}")
        print(f"Details: {e}")
        print("\nTroubleshooting:")
        print("1. Check that the GPS module is connected to /dev/ttyUSB0")
        print("2. Verify you have permission to access the serial port")
        print("   Run: sudo usermod -a -G dialout $USER")
        print("   Then log out and back in")
        print("3. Check if another program is using the port")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nExiting GPS reader...")
        ser.close()
        sys.exit(0)
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if 'ser' in locals():
            ser.close()
        sys.exit(1)

if __name__ == "__main__":
    main()

