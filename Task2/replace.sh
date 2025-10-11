#!/bin/bash

array=(
    '\[[0-9]*\]/'
    'Skywalker/Iunpwsd'
    'Luke/Johh'
    'luke/john'
    'Jedi/Kunfu'
    'Anakin/Ulugbek'
    'Padmé/Kira'
    'Amidala/Unadsf'
    'Solo/Mono'
    'Leia/Zina'
    'Organa/Tsasdf'
    'Han/Batyi'
    'Alderaan/Aldebaran'
    'Tatooine/Kabool'
    'Obi-Wan/One-Two'
    'Kenobi/Sliansf'
    'Yavin/Viyan'
    'Star/Ball'
    'Yoda/Yeji'
    'Endor/Doren'
    'Sith/Black'
    'Darth/Vlad'
    'Vader/Cepetsh'
    'Sidious/Sirius'
    'Kloss/Kolos'
    'R2-D2/E2-E4'
    'Clone/Doll'
    'Mos/Spb'
    'Anchorhead/Hoadfnio'
    'HoloNet/YahooNet'
    'Owen/Octo'
    'skyhopper/hoolahoop'
    'Jabba/Jaber'
    'Chewbacca/Dude'
    'Falcon/Duck'
    'Horox/Borox'
    'Kezarat/Teseract'
    'Mimban/Mumbai'
)

# replace
dir=knowledge_base

for filename in ${dir}/*.txt; do
    echo ${filename}
    for item in ${array[*]}; do
        sed -i "s/${item}/g" ${filename}
    done
done