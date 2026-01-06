# This file will change the dates and times of files in a specified directory.
import os
from datetime import datetime
import time
from PIL import Image
import piexif
import subprocess

def update_exif_date(file_path, new_datetime):
    """Update EXIF date for JPG files"""
    try:
        img = Image.open(file_path)
        
        # Get existing EXIF data or create new
        if 'exif' in img.info:
            exif_dict = piexif.load(img.info['exif'])
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
        
        # Format: "YYYY:MM:DD HH:MM:SS"
        date_str = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
        
        # Update EXIF date fields
        exif_dict['0th'][piexif.ImageIFD.DateTime] = date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_str
        
        # Save EXIF data
        exif_bytes = piexif.dump(exif_dict)
        img.save(file_path, exif=exif_bytes)
        return True
    except Exception as e:
        print(f"  Error updating EXIF for {os.path.basename(file_path)}: {e}")
        return False

def update_mp4_date(file_path, new_datetime):
    """Update creation date for MP4 files using exiftool"""
    try:
        date_str = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
        # Use exiftool to update MP4 metadata
        subprocess.run([
            'exiftool',
            f'-CreateDate={date_str}',
            f'-ModifyDate={date_str}',
            f'-TrackCreateDate={date_str}',
            f'-TrackModifyDate={date_str}',
            f'-MediaCreateDate={date_str}',
            f'-MediaModifyDate={date_str}',
            '-overwrite_original',
            file_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error updating MP4 metadata for {os.path.basename(file_path)}: {e}")
        return False
    except FileNotFoundError:
        print(f"  exiftool not found. Install it from https://exiftool.org/")
        return False

# Function to change the modification and access times of files in a directory. We will get the time of the file and add years, months, days, hours, minutes to it.
def change_file_dates(directory, end_date):
    # First pass: find the earliest modification time
    earliest_mod_time = None
    file_times = {}
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_datetime = datetime.fromtimestamp(mod_time)
            file_times[file_path] = mod_datetime
            
            if earliest_mod_time is None or mod_datetime < earliest_mod_time:
                earliest_mod_time = mod_datetime
    
    if earliest_mod_time is None:
        print("No files found in directory")
        return
    
    print(f"Earliest file time: {earliest_mod_time}")
    print(f"Target start time: {end_date}")
    print()
    
    # Second pass: update file times based on offset from earliest
    for file_path, mod_datetime in file_times.items():
        filename = os.path.basename(file_path)
        
        # Calculate time difference from earliest file
        time_offset = mod_datetime - earliest_mod_time
        
        # Calculate new modification time: target start + offset
        new_mod_datetime = end_date + time_offset
            
        # Convert back to timestamp
        new_mod_time = time.mktime(new_mod_datetime.timetuple())
        
        # Update the file times
        os.utime(file_path, (new_mod_time, new_mod_time))
        print(f"Updated {filename}: {mod_datetime} → {new_mod_datetime}")
        
        # Update EXIF metadata based on file type
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in ['.jpg', '.jpeg']:
            if update_exif_date(file_path, new_mod_datetime):
                print(f"  ✓ Updated EXIF metadata")
        elif file_ext == '.mp4':
            if update_mp4_date(file_path, new_mod_datetime):
                print(f"  ✓ Updated MP4 metadata")


if __name__ == "__main__":
    # Example usage: Change dates of files in 'example_directory' by adding 1 year, 2 months, 3 days, 4 hours, and 5 minutes
    directory = r"C:\Users\fkjn\Downloads\2026_Nordic MS2015 - Copy"  # Replace with your directory path

    # Set the start of the end date we want to change the files to
    end_date = datetime(2026, 1, 5, 10, 0)

    change_file_dates(directory, end_date)