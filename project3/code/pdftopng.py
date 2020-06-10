from pdf2image import convert_from_path


#filenames = ["CP1_signal_fit", "CP1_bkg_only_fit", "CP1_bkg_subtracted", "CP1_sb_fit", "CP1_dPhi", "CP1_PtEtaE"]
filenames = ["CP1_stacked_histograms"]
def convert(filename):
    pdf_file = convert_from_path("output/figures/{}.pdf".format(filename))

    for img in pdf_file:
        img.save("../Presentation/{}.png".format(filename), "PNG")


for file in filenames:
    convert(file)
