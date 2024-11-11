from sardine import SardinePdf, PdfImage

pdf = PdfImage("./invoices/invoice_1.pdf", 62, 246, output_folder="examples")

init = pdf.pdf_to_images()
pdf.save_images("init")

base = pdf.pdf_to_images(2)
pdf.save_images("base")

s1 = pdf.shake(base[0], 0)
s2 = pdf.shake(base[0], 1)
pdf.save_images("base_shake", [s1, s2])

sp = pdf.superpose_images(s1, s2)
pdf.save_images("base_shake_result", [sp])

sr = sp.resize((sp.width // 3, sp.height // 3))

sbw = pdf.convert_to_black_and_white(sr)
oot = pdf.reduce(sbw)
pdf.save_images("oot", [oot])

pdf.explore(oot)
pdf.save_images("oot_boxes", [pdf.draw_boxes(oot)])

pdf.save_images("base_boxes", [pdf.draw_boxes(base[0], 6)])

pdf.save_images("init_boxes", [pdf.draw_boxes(init[0], 12)])
pdf.extract_boxes(init[0], 12)

# pdf = SardinePdf("./invoices/invoice_1.pdf", output_folder="blablabla", debug=True)
# pdf.open()
# pdf.shake()
# pdf.binary()
# pdf.reduce(2)
# pdf.explore()
# pdf.draw()