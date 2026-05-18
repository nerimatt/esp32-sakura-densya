def create_web_page():
    with open("webClient/index.html", "r") as htmlfile:
        html = "\n".join(htmlfile.readlines())
    
    # inject javascript in webpage
    with open("webClient/index.js", "r") as jsfile:
        
        html = html.replace(
            "<!-- inject js -->",
            "<script>" + "\n".join(jsfile.readlines()) + "</script>"
        )

    # inject css
    with open("webClient/main.css", "r") as jsfile:
        
        html = html.replace(
            "/* inject css */",
            "\n".join(jsfile.readlines())
        )


    return html