# avatar-parts
Contains svg parts to generate emoji-style bust avatars

# Contributing

Fork this repository on github and clone your fork locally.

We made a [template.svg](template.svg) with inkscape. This template contains layers named [part]_box for each part. These templates show the bounding box of each part.

There are also layers named [part]_0000 that contains a default template part for each part.

You should make your own parts in separate layers named [part]_[n] with *part* being the part name (bust, ears, eyes, ...) and *n* being a **3 digits** number (or lower) if you are making a new part. If you are modifying an existing part, you should use the **4 digits** number assigned to your part.

When your layers are ready, run the python 3 script [extract_svg.py](extract_svg.py).

`extract_svg.py src_svg dst_folder author tags`

*src_svg* is your svg file containing parts as layers

*dst_folder* is the output folder (the parts folder)

*author* will be added as metadata to your parts

*tags* is a comma-separated list of keywords that will be added as metadata to your parts

The script will extract your layers and assign a **4 digit** number to each of your parts, add author and tags metadata inline, and place your part in the correct folder. If you used **4 digit** in a layer name, the corresponding part will be updated instead of being assigned a new number.

Before making a pull request, run the python 3 script [gen_indexes.py](gen_indexes.py).

`gen_indexes.py`

The script has no arguments and will build the static indexes containing the list of parts in each part folder.

Commit and push everything to your fork.

You can now make a pull request to integrate your new parts to the main repository.

# License
Code is licensed under GPL-3.0 unless stated otherwise

Medias are licensed under CC-BY-4.0 unless stated otherwise