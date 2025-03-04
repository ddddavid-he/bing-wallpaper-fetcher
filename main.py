import os
import time
import argparse
import requests
import pandas as pd
import FileOperations as file_op
from HTMLGenerator import Generator



database = "./source_list.csv"
img_dir = "./wallpaper/images"
subpages_dir = "./wallpaper/subpages"
cache_dir = "./cache"
backup_dir = "./backup"
# re_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10"
re_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&nc=1614319565639&pid=hp&FORM=BEHPTB&uhd=1"
url_base = "https://cn.bing.com"
img_prefix = "BW"
MSG_LEN = 50


def get_current_time():
    """Get current time in HH:MM:SS format.
    
    Returns:
        str: Formatted time string
    """
    return time.strftime('%H:%M:%S')


def notify(message):
    """Print formatted notification message with timestamp.
    
    Args:
        message (str): Message to display
    """
    print(f'-> ({get_current_time()}) {message}')




def create_parser():
    """Create and configure the argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Bing Wallpaper Fetcher',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--image-only', action='store_true', 
        help='Download images only'
    )
    group.add_argument(
        '--html-only', action='store_true',
        help='Generate HTML only'
    )
    
    parser.add_argument(
        '--update', action='store_true', 
        help='Update database only'
    )
    parser.add_argument(
        '--keep-cache', action='store_true',
        help='Keep temporary files'
    )
    parser.add_argument(
        '--no-image', action='store_true',
        help='Do not download images'
    )
    parser.add_argument(
        '--no-html', action='store_true',
        help='Do not generate HTML'
    )
    parser.add_argument(
        '--no-fetch', action='store_true',
        help='Do not update source_list'
    )
    parser.add_argument(
        '--no-history', action='store_true',
        help='Caution! Stop using and overwrite existing source list.'
    )
    parser.add_argument(
        '--column-number', type=int, default=3,
        help='Number of images per row in HTML'
    )
    parser.add_argument(
        '--use-wget', action='store_true',
        help='Use system wget to download data'
    )
    return parser


def validate_arguments(args):
    """Validate command line arguments and set operation flags.
    
    Args:
        args (Namespace): Parsed command line arguments
        
    Returns:
        tuple: (download_images, generate_html) flags
    """
    # Handle mutually exclusive options
    if args.image_only and args.html_only:
        raise ValueError("--image-only and --html-only are mutually exclusive")
        
    if args.image_only:
        return (True, False)
    if args.html_only:
        return (False, True)
        
    # Handle normal mode
    download = not args.no_image
    generate = not args.no_html
    
    if args.update:
        return (False, False)
        
    return (download, generate)


def ensure_directory(path):
    """Create directory if it doesn't exist.
    
    Args:
        path (str): Directory path to check/create
    """
    if not os.path.exists(path):
        os.makedirs(path)
        notify(f"Created directory: {path}")


def load_database(database_path: str, no_history: bool) -> pd.DataFrame:
    """Load and validate local database
    
    Args:
        database_path (str): Path to database file
        no_history (bool): Whether to ignore history
        
    Returns:
        pd.DataFrame: Database content with required fields
        
    Raises:
        FileNotFoundError: When --no-fetch is enabled and database doesn't exist
    """
    required_columns = ['date', 'title', 'url', 'description']
    
    if os.path.exists(database_path) and not no_history:
        try:
            df = pd.read_csv(database_path, encoding='utf-8')
            # Verify if columns exist
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                notify(f"Database missing required fields: {', '.join(missing_cols)}")
                return pd.DataFrame(columns=required_columns)
            return df[required_columns].astype({'date': str})
        except Exception as e:
            notify(f"Failed to load database: {str(e)}")
            return pd.DataFrame(columns=required_columns)
    
    if args.no_fetch:
        raise FileNotFoundError("No existing database found when --no-fetch is enabled")
        
    return pd.DataFrame(columns=required_columns)


def update_database(existing_df: pd.DataFrame) -> pd.DataFrame:
    """Fetch latest data from Bing API and update database
    
    Args:
        existing_df (pd.DataFrame): Existing database content
        
    Returns:
        pd.DataFrame: Updated database
        
    Raises:
        requests.HTTPError: When API request fails
    """
    try:
        notify('Requesting Bing API...')
        response = requests.get(re_url)
        response.raise_for_status()
        image_data = response.json()['images']
        notify('API response received successfully')
    except requests.RequestException as e:
        notify(f"API request failed: {str(e)}")
        raise

    # Convert API data to DataFrame
    new_records = [{
        'date': img['enddate'],
        'title': img['title'],
        'url': f"{url_base}{img['urlbase']}_UHD.jpg",
        'description': img['copyright']
    } for img in image_data]

    new_df = pd.DataFrame(new_records).astype({'date': str})
    
    # Merge new and existing data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    # Remove duplicates and sort
    combined_df = (
        combined_df
        .drop_duplicates(subset=['date'], keep='first')
        .sort_values('date', ascending=False)
        .reset_index(drop=True)
    )
    
    # Save updates
    try:
        combined_df.to_csv(database, index=False, encoding='utf-8')
        new_count = len(new_df) - (len(combined_df) - len(existing_df))
        notify(f"Added {new_count} new records, total count: {len(combined_df)}")
    except IOError as e:
        notify(f"Failed to save database: {str(e)}")
    
    return combined_df


def download_images_task(src_df, img_dir, cache_dir, img_prefix, use_wget):
    """Execute image download task
    
    Args:
        src_df (DataFrame): DataFrame containing image information
        img_dir (str): Directory to save images
        cache_dir (str): Cache directory
        img_prefix (str): Image filename prefix
        use_wget (bool): Whether to use wget for downloading
    """
    downloaded_imgs = os.listdir(img_dir)
    
    for date_str, url in zip(src_df['date'], src_df['url']):
        try:
            target_file = f'{img_prefix}-{date_str[2:]}.jpg'
            if target_file in downloaded_imgs:
                continue
                
            cache_file = f'{cache_dir}/img_cache'
            
            if use_wget:
                os.system(f'wget -q -O {cache_file} {url}')
            else:
                response = requests.get(url)
                response.raise_for_status()
                with open(cache_file, 'wb') as f:
                    f.write(response.content)
            
            file_op.move_files(
                cache_file, 
                os.path.join(img_dir, target_file)
            )
            notify(f'{target_file} downloaded')
            
        except Exception as e:
            notify(f"Download failed for {target_file}: {str(e)}")

def generate_html_task(src_df, subpages_dir, column_number):
    """Execute HTML generation task
    
    Args:
        src_df (DataFrame): DataFrame containing image information
        subpages_dir (str): Directory to save subpages
        column_number (int): Number of images per column
    """
    try:
        hg = Generator(
            src_df['date'], 
            src_df['url'], 
            src_df['title'], 
            src_df['description'],
            col=column_number
        )
        
        num = hg.generate_all()
        
        # Generate main page
        with open(f'{cache_dir}/index.html', 'w', encoding='utf8') as f:
            f.write(hg.mainpage)
        
        # Generate subpages
        for key in hg.subpages.keys():
            with open(f'{cache_dir}/page-{key}.html', 'w', encoding='utf8') as f:
                f.write(hg.subpages[key])
        
        # Move generated files
        if num > 0:
            file_op.copy_files(f'{cache_dir}/index.html', 'wallpaper/')
            file_op.copy_files(f'{cache_dir}/page-*.html', subpages_dir)
            
        notify(f'Successfully generated wallpaper/index.html')
        notify(f'Generated {num} subpages to {subpages_dir}/')
        
    except Exception as e:
        notify(f"HTML generation failed: {str(e)}")
        raise


if __name__ == "__main__":

    # Initialize argument parser
    parser = create_parser()
    args = parser.parse_args()

    try:
        download_images, generate_html = validate_arguments(args)
    except ValueError as e:
        print(f"Argument error: {e}")
        parser.print_help()
        exit(1)

    # Create required directories
    required_dirs = [img_dir, subpages_dir, cache_dir, backup_dir]
    for directory in required_dirs:
        ensure_directory(directory)



    print('>' * MSG_LEN)
    print('\t', time.ctime())
    print('>' * MSG_LEN)


    # Load existing database
    try:
        src = load_database(database, args.no_history)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        exit(1)

    # Update database (if not skipped)
    if not args.no_fetch:
        try:
            src = update_database(src)
        except requests.HTTPError:
            notify("Continuing with local database")



    # Execute image download task
    if download_images:
        try:
            download_images_task(src, img_dir, cache_dir, img_prefix, args.use_wget)
        except Exception as e:
            print(f"Image download task failed: {str(e)}")
            exit(1)

    # Execute HTML generation task
    if generate_html:
        try:
            generate_html_task(src, subpages_dir, args.column_number)
        except Exception as e:
            print(f"HTML generation task failed: {str(e)}")
            exit(1)


    if not args.keep_cache:

        try:
            file_op.remove_files(f'{cache_dir}/img_cache')
            file_op.remove_files(f'{cache_dir}/*.html')
            notify("Cache files cleaned")
        except Exception as e:
            notify(f"Failed to clean cache: {str(e)}")
    else:
        notify("Cache files retained")

    print('<' * MSG_LEN, end='\n\n')

    exit(0)
