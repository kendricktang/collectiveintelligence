from PIL import Image, ImageDraw


def printhclust(clust, labels=None, n=0):
    # Indent to make a hierarchy layout
    for i in range(n):
        print ' ',
    if clust.id < 0:
        # negative id means this is a branch
        print '-'
    else:
        # positive id means this is a leaf
        if labels is None:
            print clust.id
        else:
            print labels[clust.id]

    # Now print branches
    if clust.left is not None:
        printhclust(clust.left, labels=labels, n=n+1)
    if clust.right is not None:
        printhclust(clust.right, labels=labels, n=n+1)


def getheight(clust):
    if clust.left is None and clust.right is None:
        return 1

    return getheight(clust.left)+getheight(clust.right)


def getdepth(clust):
    if clust.left is None and clust.right is None:
        return 0

    return max(getdepth(clust.left), getdepth(clust.right))+clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # Get dimensions
    height = getheight(clust)*20
    width = 1200
    depth = getdepth(clust)

    # width is fixed so scale the distances accordingly
    scaling = float(width-150)/depth

    # create new image with white background
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, height/2, 10, height/2), fill=(255, 0, 0))

    # Draw the first node
    drawnode(draw, clust, 10, (height/2), scaling, labels)
    img.save(jpeg, 'JPEG')


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        # This is a branch node
        h1 = getheight(clust.left)*20
        h2 = getheight(clust.right)*20
        top = y-(h1+h2)/2
        bottom = y+(h1+h2)/2

        # Line length
        linelength = clust.distance*scaling

        # Vertical line from this cluster to its children
        draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255, 0, 0))

        # Horizontal line to the left child
        draw.line((x, top+h1/2, x+linelength, top+h1/2), fill=(0, 255, 0))

        # Horizontal line to the right child
        draw.line((x, bottom-h2/2, x+linelength, bottom-h2/2), fill=(0, 0, 255))

        # Call recursion
        drawnode(draw, clust.left, x+linelength, top+h1/2, scaling, labels)
        drawnode(draw, clust.right, x+linelength, bottom-h2/2, scaling, labels)
    else:
        # This is a leaf node
        draw.text((x+5, y-7), labels[clust.id], fill=(0, 0, 0))
