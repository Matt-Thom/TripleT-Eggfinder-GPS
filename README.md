# TripleT-Eggfinder-GPS

My Eggfinder GPS Test bed and other Eggfinder GPS software.

## Project Status

**Current Stage**: Active Development - GPS Reader Implementation

This project is in active development. The GPS reader module is complete and functional, capable of reading and parsing NMEA sentences from Eggfinder GPS modules.

### Completed Features
- ✅ GPS serial communication module (`gps_reader.py`)
- ✅ NMEA sentence parsing (GPGGA and GPRMC)
- ✅ Real-time GPS data display
- ✅ Coordinate conversion to decimal degrees
- ✅ Speed and course tracking
- ✅ Altitude and satellite information display

## What's Coming Up

- Data logging and storage functionality
- GPS track visualization
- Advanced Eggfinder GPS features integration
- Web-based monitoring interface
- Flight data analysis tools

## How to Use

### GPS Reader

The GPS reader connects to an Eggfinder GPS module via USB serial and displays real-time GPS data.

#### Requirements
- Python 3.x
- pyserial library
- GPS module connected to `/dev/ttyUSB0` at 9600 baud

#### Installation
```bash
pip install -r requirements.txt
```

#### Running the GPS Reader
```bash
python3 gps_reader.py
```

The script will display:
- Current position (latitude/longitude in decimal degrees)
- GPS time (UTC)
- Fix quality and number of satellites
- Altitude above sea level
- Speed (in knots, km/h, and mph)
- Course/heading in degrees

Press `Ctrl+C` to exit.

#### Troubleshooting
If you get a permission error accessing `/dev/ttyUSB0`:
```bash
sudo usermod -a -G dialout $USER
```
Then log out and back in for the changes to take effect.

### Documentation System

This project maintains high-quality documentation through automated monitoring and maintenance. All documentation follows strict Markdown format standards.

### Documentation Standards
- See `AI_Rules.md` for complete documentation rules and standards
- All documentation files must use `.md` extension
- Python docstrings must use Markdown formatting
- Documentation must stay synchronized with code changes

### Documentation Agent
- See `DOCUMENTATION_AGENT_PROMPT.md` for the Documentation Agent prompt
- The Documentation Agent continuously monitors and maintains project documentation
- Ensures all documentation follows Markdown format standards
- Keeps documentation synchronized with codebase changes

### Coding Agent Notification Protocol
- See `CODING_AGENT_NOTIFICATION_PROTOCOL.md` for notification guidelines
- Coding Agents should notify the Documentation Agent when code changes require documentation updates
- Includes templates and examples for proper notification format
- Ensures documentation stays current with code changes

## Project Files

### Core Application
- `gps_reader.py` - GPS data reader and parser for Eggfinder GPS modules
- `requirements.txt` - Python package dependencies

### Documentation
- `AI_Rules.md` - Core coding and documentation standards
- `DOCUMENTATION_AGENT_PROMPT.md` - Documentation Agent role and responsibilities
- `CODING_AGENT_NOTIFICATION_PROTOCOL.md` - Protocol for code-to-documentation communication
- `README.md` - This file, project overview and documentation

