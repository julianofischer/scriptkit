#!/bin/bash
while read line; do
        TITLE=$(echo "$line" | cut -f1)
        AREA=$(echo "$line" | cut -f3)
        URL=$(echo "$line" | cut -f4)
        directory=$AREA
        filename="${TITLE}.pdf"
        destination="${directory}/$filename"
        mkdir -p "$directory"
        substitute="content/pdf/10.1007%2F"
        novaurl=${URL//openurl?genre=book&isbn=/$substitute}
        wget "$novaurl" -O "$destination"
done < planilha.tsv
