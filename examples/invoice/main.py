from sardine import SardinePdf

output_folder = "./examples/invoice/output/"

sardine = SardinePdf("./examples/invoice/invoice.pdf", debug=True)
pages = sardine.get_pages()

for page in pages:
    images = page.get_images()
    images[1][0].save(output_folder, "invoice")
    ini = page.add_image()
    images[1][ini].binarization()
    images[1][ini].save(output_folder, "invoice_binarization")
    
    resize = 2
    ini = page.add_image(resize, (1, ini))
    images[resize][ini].save(output_folder, "invoice_binarization_resize")

    size = 1
    ini = page.add_image(resize, (size, 0))
    images[resize][ini].save(output_folder, "invoice_resize")
    images[resize][ini].shake(1)
    images[resize][ini].save(output_folder, "invoice_resize_shake")

    ini = page.add_image(resize, (resize, ini))
    images[resize * resize][ini].binarization()
    images[resize * resize][ini].save(output_folder, "invoice_resize_shake_resize_binarization")

    utltima_resize = 3
    ini = page.add_image(utltima_resize, (resize * resize, ini))
    images[resize * resize * utltima_resize][ini].binarization()
    images[resize * resize * utltima_resize][ini].save(output_folder, "invoice_resize_shake_resize_binarization_resize_binarization")