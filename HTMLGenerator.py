"""
HTML Generator for Bing Wallpaper Gallery.

This module provides functionality to generate HTML pages for displaying
Bing wallpaper images in a responsive gallery format.
"""
from typing import List, Tuple, Dict, Optional


class Generator:
    """
    Generator class for creating HTML pages to display Bing wallpaper images.
    
    This class handles the generation of a main gallery page and individual
    subpages for each wallpaper with its details.
    """
    
    # Constants for HTML structure
    SMALL_IMAGE_REQUEST = "&rf=LaDigue_UHD.jpg&pid=hp&w=WIDTH&h=HEIGHT&rs=1&c=4"
    DEFAULT_RESOLUTION = (384, 216)
    
    def __init__(
        self, 
        dates: List[str], 
        urls: List[str], 
        titles: List[str], 
        descriptions: List[str], 
        col: int = 3, 
        today_size: int = 70
    ):
        """
        Initialize the Generator with wallpaper data and layout settings.
        
        Args:
            dates: List of dates for each wallpaper (format: YYMMDD or YYYYMMDD)
            urls: List of URLs to the wallpaper images
            titles: List of titles for each wallpaper
            descriptions: List of descriptions for each wallpaper
            col: Number of columns to display in the gallery (default: 3)
            today_size: Width percentage for today's featured image (default: 70)
        """
        self.dates = dates
        self.urls = urls
        self.titles = titles
        self.descriptions = descriptions
        self.col = col
        self.today_size = today_size
        self.mainpage: Optional[str] = None
        self.subpages: Dict[str, str] = {}
        
        # HTML template parts
        self.head = self._create_header()
        self.tail = self._create_footer()
        
    def _create_header(self) -> str:
        """Create the HTML header section."""
        header = [
            "<!DOCTYPE html>",
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">',
            "<head>",
            "\t<meta charset=\"utf-8\"/>",
            "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=yes\"/>",
            "\t<title>Bing Wallpaper Gallery</title>",
            "\t<style type=\"text/css\">",
            "\t\tcode { white-space: pre-wrap; }",
            "\t\tspan.smallcaps { font-variant: small-caps; }",
            "\t\tspan.underline { text-decoration: underline; }",
            "\t\tdiv.column { display: inline-block; vertical-align: top; width: 50%; }",
            "\t</style>",
            "</head>",
            '<body>',
            '<a id="top"></a>',
            "<br>",
            "<hr>",
            "<br>",
            "<h1 align=\"center\">Bing Wallpaper Gallery</h1>",
            "<br>",
            "<hr>",
            "<br>",
        ]
        return "\n".join(header)
        
    def _create_footer(self) -> str:
        """Create the HTML footer section with CSS styles."""
        # Calculate the item width based on columns with proper spacing
        item_width = f"{(100-10)/self.col}%"
        
        footer = [
            "\t<p class=\"bottom-space\"></p>",
            "",
            "\t<hr>",
            "\t<br>",
            "\t<nav>",
            "\t<h4 align=\"center\">",
            "\t\t<a href=\"#top\">Back To Top</a>",
            "\t\t&nbsp;",
            "\t\t<a href=\"https://cn.bing.com\">See Bing Here</a>",
            "\t</h4>",
            "\t<br>",
            "\t</nav>",
            "",
            "</body>",
            "",
            "<style>",
            "\t* {",
            "\t\tmargin: 0;",
            "\t\tpadding: 0;",
            "\t}",
            "\t.row-container {",
            "\t\twidth: 100%;",
            "\t\tdisplay: flex;",
            "\t\tflex-wrap: wrap;",
            "\t\tmargin-top: 20px;",
            "\t\tjustify-content: center;",
            "\t}",
            "\t.item-container {",
            f"\t\twidth: {item_width};",
            "\t\theight: auto;",
            "\t\tvertical-align: middle;",
            "\t\tmargin: 1px auto;",
            "\t}",
            "\t.today-item-container {",
            f"\t\twidth: {self.today_size}%;",
            "\t\theight: auto;",
            "\t\tvertical-align: middle;",
            "\t\tmargin: 1px auto;",
            "\t\tmargin-bottom: 5px;",
            "\t}",
            "",
            "\t.img-container {",
            "\t\twidth: 100%;",
            "\t\theight: auto;",
            "\t}",
            "\timg {",
            "\t\twidth: 100%;",
            "\t\theight: auto;",
            "\t\tborder-radius: 4px;",
            "\t}",
            "\t.img-title {",
            "\t\tpadding: 10px 0;",
            "\t\ttext-align: center;",
            "\t\tfont-size: 16px;",
            "\t\tfont-weight: normal;",
            "\t}",
            "\t.bottom-space {",
            "\t\tmargin-bottom: 1cm;",
            "\t}",
            "</style>",
            "",
            "</html>"
        ]
        return "\n".join(footer)

    def gen_item(self, date: str, url: str, lazy: bool = False, resolution: Tuple[int, int] = None) -> str:
        """
        Generate HTML for a single gallery item.
        
        Args:
            date: Date of the wallpaper (format: YYMMDD)
            url: URL to the wallpaper image
            lazy: Whether to use lazy loading for the image (default: False)
            resolution: Image resolution as (width, height) (default: class default)
            
        Returns:
            HTML code for the gallery item
        """
        if resolution is None:
            resolution = self.DEFAULT_RESOLUTION
            
        full_date = f"20{date[:2]}-{date[2:4]}-{date[4:]}"
        small_url = f"{url}{self.SMALL_IMAGE_REQUEST}"
        small_url = small_url.replace('WIDTH', str(resolution[0]))
        small_url = small_url.replace('HEIGHT', str(resolution[1]))
        subpage = f"subpages/page-{date}.html"
        
        loading_attr = "loading=\"lazy\"" if lazy else ""
        
        # Build the HTML for this gallery item
        html_parts = [
            "\t<div class=\"item-container\">",
            "\t\t<div class=\"img-container\">",
            f"\t\t<a href=\"{subpage}\" target=\"_blank\">",
            f"\t\t\t<img src=\"{small_url}\" alt=\"Bing wallpaper\" {loading_attr} width=\"{resolution[0]}\" height=\"{resolution[1]}\">",
            "\t\t</a>",
            "\t\t</div>",
            "\t\t<h5 class=\"img-title\">",
            f"\t\t\t{full_date} &nbsp;",
            f"\t\t\t<a href=\"{subpage}\" target=\"_blank\">See Details</a> &nbsp;",
            f"\t\t\t<a href=\"images/BW-{date}.jpg\" download>Download</a>",
            "\t\t</h5>",
            "\t</div>"
        ]
        
        return "\n".join(html_parts)

    def gen_today(self) -> str:
        """
        Generate HTML for today's featured wallpaper.
        
        Returns:
            HTML code for today's wallpaper section
        """
        description = self.descriptions[0]
        date = self.dates[0][2:] if len(self.dates[0]) > 6 else self.dates[0]
        url = self.urls[0]
        small_url = url.replace('UHD', '1920x1080')
        
        html_parts = [
            "\t<div class=\"today-item-container\">",
            "\t\t<div class=\"img-container\">",
            f"\t\t\t<a href=\"subpages/page-{date}.html\" target=\"_blank\">",
            f"\t\t\t\t<img src=\"{small_url}\" alt=\"Today's Bing wallpaper\">",
            "\t\t\t</a>",
            "\t\t</div>",
            "\t\t<h3 class=\"img-title\">",
            f"\t\t\t<b>Today: </b>{description}",
            "\t\t</h3>",
            "\t</div>"
        ]
        
        return "\n".join(html_parts)

    def gen_row(self, items: List[str]) -> str:
        """
        Generate HTML for a row of gallery items.
        
        Args:
            items: List of HTML item codes to include in this row
            
        Returns:
            HTML code for the row container with items
        """
        if not items:
            return ""
            
        html_parts = ["<div class=\"row-container\">"]
        html_parts.extend(items)
        html_parts.append("</div>")
        
        return "\n".join(html_parts)

    def gen_main_page(self) -> str:
        """
        Generate the main gallery page HTML.
        
        Returns:
            Complete HTML for the main gallery page
        """
        # Start with the header and today's featured image
        html_content = []
        html_content.append(self.head)
        html_content.append(self.gen_row([self.gen_today()]))
        
        # Calculate rows and columns
        num_images = len(self.dates)
        col = self.col
        row_num = num_images // col
        
        # Generate rows of gallery items
        for i in range(row_num):
            items = []
            # Use lazy loading for images further down the page
            lazy_load = i > 10
            
            for j in range(col):
                idx = i * col + j
                if idx >= len(self.dates):
                    break
                    
                date = self.dates[idx][2:] if len(self.dates[idx]) > 6 else self.dates[idx]
                url = self.urls[idx]
                items.append(self.gen_item(date, url, lazy=lazy_load))
                
            if items:
                html_content.append(self.gen_row(items))
        
        # Handle remaining images (if not evenly divisible by column count)
        remaining = num_images % col
        if remaining > 0:
            items = []
            for j in range(remaining):
                idx = row_num * col + j
                if idx >= len(self.dates):
                    break
                    
                date = self.dates[idx][2:] if len(self.dates[idx]) > 6 else self.dates[idx]
                url = self.urls[idx]
                items.append(self.gen_item(date, url, lazy=True))
                
            if items:
                html_content.append(self.gen_row(items))
        
        # Add footer
        html_content.append(self.tail)
        
        # Save and return the complete HTML
        self.mainpage = "\n".join(html_content)
        return self.mainpage

    def gen_subpage(self, date: str, url: str, title: str, description: str) -> str:
        """
        Generate HTML for an individual wallpaper subpage.
        
        Args:
            date: Date of the wallpaper (format: YYYYMMDD or YYMMDD)
            url: URL to the wallpaper image
            title: Title of the wallpaper
            description: Description of the wallpaper
            
        Returns:
            Complete HTML for the subpage
        """
        # Format the date
        if len(date) == 8:  # YYYYMMDD format
            long_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            short_date = date[2:]
        else:  # YYMMDD format
            long_date = f"20{date[:2]}-{date[2:4]}-{date[4:]}"
            short_date = date
        
        html_parts = [
            "<!DOCTYPE html>",
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">',
            "<head>",
            "\t<meta charset=\"utf-8\">",
            "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=yes\"/>",
            f"\t<title>Bing Wallpaper - {long_date}</title>",
            "\t<style>",
            "\t\t* { margin: 0; padding: 0; }",
            "\t\tbody { font-family: Arial, sans-serif; line-height: 1.6; }",
            "\t\t.container { width: 90%; max-width: 1200px; margin: 40px auto; }",
            "\t\t.wallpaper-image { width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }",
            "\t\t.wallpaper-info { margin-top: 20px; text-align: center; }",
            "\t\t.download-btn { display: inline-block; background: #0078d7; color: white; padding: 8px 16px; ",
            "\t\t                text-decoration: none; border-radius: 4px; margin-top: 15px; }",
            "\t\t.download-btn:hover { background: #005a9e; }",
            "\t</style>",
            "</head>",
            "",
            "<body>",
            "\t<div class=\"container\">",
            "\t\t<div>",
            f"\t\t\t<img class=\"wallpaper-image\" src=\"{url}\" alt=\"{title}\" loading=\"lazy\">",
            "\t\t</div>",
            "",
            "\t\t<div class=\"wallpaper-info\">",
            "\t\t\t<h3>",
            f"\t\t\t\t「{title}」:&nbsp;",
            f"\t\t\t\t{description}",
            f"\t\t\t\t<a href=\"../images/BW-{short_date}.jpg\" download>",
            "\t\t\t\t\tDownload",
            "\t\t\t\t</a>",
            "\t\t\t</h3>",
            "\t\t</div>",
            "\t</div>",
            "</body>",
            "</html>"
        ]
        
        # Save the subpage content and return it
        html_content = "\n".join(html_parts)
        self.subpages[short_date] = html_content
        return html_content
    
    def generate_all(self) -> int:
        """
        Generate all HTML pages (main page and subpages).
        
        Returns:
            Number of pages generated
        """
        self.gen_main_page()
        
        for i, date in enumerate(self.dates):
            self.gen_subpage(
                date,
                self.urls[i],
                self.titles[i],
                self.descriptions[i]
            )
        
        return len(self.dates) + 1  # Main page + all subpages
