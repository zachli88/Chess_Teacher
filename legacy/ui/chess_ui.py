import webview

def main():
    webview.create_window("chess ai", "../web/templates/index.html")
    webview.start()

if __name__ == "__main__":
    main()