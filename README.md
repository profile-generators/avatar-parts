# avatar-parts
Contains svg parts to generate emoji-style bust avatars

# Contributing

## Setup your workspace

Fork this repository on github and clone your fork locally.

We made a [template.svg](template.svg) with inkscape. This template contains layers named [part]_box for each part. These layers show the bounding box of each part.

There are also layers named [part]_0000 that contains a default template part for each part.

Start by copying **template.svg** to **work.svg**

You should make your own parts in separate layers named [part]_[n] with *part* being the part name (bust, ears, eyes, ...) and *n* being a **3 digits** number (or lower) if you are making a new part. If you are modifying an existing part, you should use the **4 digits** number assigned to your part.

## Working with the palette

A color palette is embeded inside *template.svg* as css classes. This is used to allow the end user to select colors for avatar parts. The palette consists of the following colors

class name | default | usage
---------- | ------- | -----
flesh      | ![#ffe7bd](resources/flesh.png "#ffe7bd") | main flesh elements
flesh2     | ![#f7cf88](resources/flesh2.png "#f7cf88") | flesh shadows
flesh3     | ![#ffdebd](resources/flesh3.png "#ffdebd") | lighter flesh
hair       | ![#803300](resources/hair.png "#803300") | main hair
hair2      | ![#383837](resources/hair2.png "#383837") | hair shadows / darker hair
eye        | ![#d8d5ff](resources/eye.png "#d8d5ff") | eye color
p1         | ![#006eb3](resources/p1.png "#006eb3") | palette 1
p2         | ![#008de6](resources/p2.png "#008de6") | palette 2
p3         | ![#00b39e](resources/p3.png "#00b39e") | palette 3
p4         | ![#00e6cb](resources/p4.png "#00e6cb") | palette 4

To use the palette with inkscape you have to open the **XML Editor** located in the *Edit* menu. You can then click on an object (or path) and set a "class" attribute with the class name (i.e. "flesh") you desire.

Although you should use the palette as much as possible, you can use hardcoded colors as well. Using black or white objects with custom opacities can be usefull to add shadows or highlights over palette colors.


## Pushing your updates
When your layers are ready, run the python 3 script [extract_svg.py](extract_svg.py).

`extract_svg.py src_svg dst_folder author tags`

*src_svg* is your svg file containing parts as layers (work.svg)

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