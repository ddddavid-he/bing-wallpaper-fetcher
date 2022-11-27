class Generator:
    def __init__(self, dates, urls, titles, descriptions, col=3, today_size=70):
        self.dates = dates
        self.urls = urls
        self.titles = titles
        self.descriptions = descriptions
        self.col = col
        self.today_size = today_size
        self.mainpage = None
        self.subpages = {}
        self.small_req = "&rf=LaDigue_UHD.jpg&pid=hp&w=WIDTH&h=HEIGHT&rs=1&c=4"
        self.head = [
                "<!DOCTYPE html>",
                "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"\" xml:lang=\"\">",
                "<head>",
                "\t<meta charset=\"utf-8\"/>",
                "\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=yes\"/>",
                "\t<title>Bing Wallpaper</title>",
                "\t<style type=\"text/css\">",
                "\t\tcode{white-space: pre-wrap;}",
                "\t\tspan.smallcaps{font-variant: small-caps;}",
                "\t\tspan.underline{text-decoration: underline;}",
                "\t\tdiv.column{display: inline-block; vertical-align: top; width: 50%;}",
                "\t</style>",
                "</head>",
                "<a name=\"top\"></a>",
                "<br>",
                "<hr>",
                "<br>",
                "<h1 align=\"center\">Bing Wallpaper  Gallery</h1>",
                "<br>",
                "<hr>",
                "<br>",
                "",
                "<body>"
        ]
        self.tail = [
            "\t\t<p class=\"bottom-space\"></p>",
            "",
            "\t\t<hr>",
            "\t\t<br>",
            "\t\t<nav>",
            "\t\t<h4 align=\"center\">",
            "\t\t\t<a href=\"\#top\">Back To Top</a>",
            "\t\t\t&nbsp;",
            "\t\t\t<a href=\"https://cn.bing.com\">See Bing Here</a>",
            "\t\t</h4>",
            "\t\t<br>",
            "\t\t",
            "\t\t</nav>",
            "\t\t",
            "\t\t<!-- <hr> -->",
            "\t\t<br>",
            "",
            "\t</body>",
            "",
            "",
            "\t<style>",
            "\t\t*{",
            "\t\t\tmargin: 0;",
            "\t\t\tpadding: 0;",
            "\t\t}",
            "\t\t.row-container{",
            "\t\t\twidth: 100%;",
            "\t\t\tdisplay: flex;",
            "\t\t\tdisplay: -webkit-flex;",
            "\t\t\tmargin-top: 20px;",
            "\t\t\t/* justify-content: space-around; */",
            "\t\t\tjustify-content: center;",
            "\t\t\t/* vertical-align: middle; */",
            "\t\t\t/* margin: 20px auto; */",
            "\t\t}",
            "\t\t.item-container{",
            f"\t\t\twidth: {(100-10)/self.col}%;",
            "\t\t\theight: auto;",
            "\t\t\tvertical-align: middle;",
            "\t\t\tmargin: 1 auto;",
            "\t\t}",
            "\t\t.today-item-container{",
            f"\t\t\twidth: {self.today_size}%;",
            "\t\t\theight: auto;",
            "\t\t\tvertical-align: middle;",
            "\t\t\tmargin: 1 auto;",
            "\t\t\tmargin-bottom: 5;",
            "\t\t}",
            "",
            "\t\t.img-container{",
            "\t\t\twidth: 100%;",
            "\t\t\theight:auto;",
            "\t\t}",
            "\t\timg{",
            "\t\t\twidth: 100%;",
            "\t\t\theight: auto;",
            "\t\t}",
            "\t\t.img-title{",
            "\t\t\tpadding: 10px 0;",
            "\t\t\ttext-align: center;",
            "\t\t\tfont-size: 16;",
            "\t\t\tfont-weight: normal;",
            "\t\t}",
            "\t\t.bottom-space {",
            "\t\t\tmargin-bottom: 1cm;",
            "\t\t}",
            "\t</style>",
            "",
            "",
            "",
            "</html>"
        ]
        self.head = "\n".join(self.head)
        self.tail = "\n".join(self.tail)
        

    def genItem(self, date, url, lazy=False, resolution=(384, 216)):
        full_date = f"20{date[:2]}-{date[2:4]}-{date[4:]}"
        # date = date[2:]
        # small_url = url.replace('UHD', '1280x720')
        small_url = f"{url}{self.small_req}"
        small_url = small_url.replace('WIDTH', str(resolution[0]))
        small_url = small_url.replace('HEIGHT', str(resolution[1]))
        subpage = f"subpages/page-{date}.html"
        if lazy:
            loading = "loading=\"lazy\""
        else:
            loading = ""
        code = ""
        code += "\t<div class=\"item-container\">\n"
        code += "\t\t<div class=\"img-container\">\n"
        code += f"\t\t<a href={subpage} target=\"_blank\">"
        code += f"\t\t\t<img src={small_url} alt=\"bing picture\" {loading} width={str(resolution[0])} height={str(resolution[1])}>\n"
        code += "\t\t</a>"
        code += "\t\t</div>\n"
        code += "\t\t<h5 class=\"img-title\">\n"
        # code += f"\t\t\t<a href=\"{url}\">{full_date}</a>\n"
        code += f"\t\t\t{full_date} &nbsp;\n"
        code += f"\t\t\t<a href={subpage} target=\"_blank\">See Details</a> &nbsp;\n"
        code += f"\t\t\t<a href=\"images/BW-{date}.jpg\" download=\"\">Download 4K</a>\n"
        code += "\t\t</h5>\n"
        code += "\t</div>\n"
        return code


    def genToday(self):
        description = self.descriptions[0]
        date = self.dates[0][2:]
        url = self.urls[0]
        # print(url)
        small_url = url.replace('UHD', '1920x1080')
        code = ""
        code += "\t<div class=\"today-item-container\">\n"
        code += "\t\t<div class=\"img-container\">\n"
        code += f"\t\t\t<a href=\"subpages/page-{date}.html\" target=\"_blank\">"
        code += f"\t\t\t\t<img src={small_url} alt=\"\">\n"
        code += "\t\t\t</a>"
        code += "\t\t</div>\n"
        code += "\t\t<h3 class=\"img-title\">\n"
        code += f"\t\t\t<b>Today: </b>{description}\n"
        code += "\t\t</h3>\n"
        code += "\t</div>\n"
        return code
        

    def genRow(self, items):
        code = ""
        code += "<div class=\"row-container\">\n"
        for item in items:
            code += item
            code += "&nbsp;"
        code = code[:-6]
        code += "</div>"
        code += "\n"
        return code


    def genMainPage(self):
        code = ""
        code += self.head
        code += self.genRow([self.genToday()])
        
        num = len(self.dates)
        col = self.col
        row_num = num // col
        for i in range(row_num):
            items = []
            if i > 10:
                lazy = True
            else:
                lazy = False
            for j in range(col):
                date = self.dates[i*col+j][2:]
                url = self.urls[i*col+j]
                items.append(self.genItem(date, url, lazy=lazy))
            code += self.genRow(items)
        if(num%col != 0):
            items = []
            for j in range(num%3):
                date = self.dates[row_num*3+j][2:]
                url = self.urls[row_num*3+j]
                items.append(self.genItem(date, url, lazy=True))
            code += self.genRow(items)
        code += "\n\n"
        code += self.tail
            
        self.mainpage = code 
        return code 
        


    def genSubpage(self, date, url, title, description):
        long_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        date = date[2:]
        code = [
            "<!DOCTYPE html>",
            "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"\" xml:lang=\"\">",
            "<head>",
            "\t<meta charset=\"utf-8\">",
            f"\t<title>{long_date}</title>",
            "</head>",
            "",
            "<br><br>",
            "<body>",
            "\t<div  style=\"",
            "\t\t\twidth: 100%;",
            "\t\t\tdisplay: flex;",
            "\t\t\tdisplay: -webkit-flex;",
            "\t\t\tmargin-top: 20px;",
            "\t\t\tjustify-content: center;\"",
            "\t>",
            "",
            "\t<div  style=\"",
            "\t\t\twidth: 90%;",
            "\t\t\theight: auto;",
            "\t\t\tvertical-align: middle;",
            "\t\t\tmargin: 1 auto\"",
            "\t>",
            "",
            "\t\t<div style=\"width: 100%;height:auto;\">",
            f"\t\t\t<img src={url} ",
            "\t\t\t\talt=\"\" width=\"100%\" height=\"auto\"",
            "\t\t\t>",
            "\t\t</div>",
            "",
            "\t\t<div style=\">",
            "\t\t\t\tpadding: 10px 0;",
            "\t\t\t\ttext-align: center;",
            "\t\t\t\tfont-size: 16;",
            "\t\t\t\tfont-weight: normal;\"",
            "\t\t>",
            "\t\t\t<h3 align=\"center\">",
            f"\t\t\t\t「{title}」:&nbsp;",
            f"\t\t\t\t{description} &nbsp;",
            f"\t\t\t\t<a href=\"../images/BW-{date}.jpg\" download=\"\">",
            "\t\t\t\t\tDownload",
            "\t\t\t\t</a>",
            "\t\t\t</h3>",
            "\t\t</div>",
            "\t</div>",
            "\t</div>",
            "</body>",
            "</html>"
        ]
        code = "\n".join(code)
        
        self.subpages[f"{date}"] = code
        return code
    
    
    def generateAll(self):
        self.genMainPage()
        num = len(self.dates)
        for i in range(num):
            self.genSubpage(
                self.dates[i],
                self.urls[i],
                self.titles[i],
                self.descriptions[i]
            )
        return num
    
    
