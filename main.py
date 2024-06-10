import src.downloader.msite as wpm

if __name__ == '__main__':
    settings = wpm.load(open("./assets/settings.json"))

    main = wpm.Site(settings)
    #myPage = main.getPageBySearch("Леса и медведи", "3440x1440")
    myPage = main.getPageBySearch("Леса и медведи")
    images = myPage.loadImages()

    print(f"Getting images from: {myPage.url}")

    if len(images) == 0:
        print(f"No wallpapers was found by query '{main.lastQuery}'")

    for i, img in enumerate(images):
        print(str(i) + ' | ' + str(img) + "\n")
    
    inx = int(input("Enter image index to download: "))

    images[inx].save("./assets/wallpapers/main.jpg", 'main')
    images[inx].save("./assets/wallpapers/preview.jpg", 'preview')