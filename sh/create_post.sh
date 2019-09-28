#!/bin/bash

# script pra criar header dos posts do Jekyll já com a data certa

nome_arquivo=$1
data_arquivo=$(date +"%Y-%m-%d")

arquivo="${data_arquivo}-${nome_arquivo}.md"

echo "Criando arquivo $arquivo"

echo "---" >> $arquivo
echo "title: " >> $arquivo
echo "layout: post" >> $arquivo
echo "date: $(date +"%Y-%m-%d %H:%M")" >> $arquivo
echo "image: " >> $arquivo
echo "headerImage: false" >> $arquivo
echo "tag: " >> $arquivo
echo "category: blog" >> $arquivo
echo "author: giovanamorais" >> $arquivo
echo "description: " >> $arquivo
echo "---" >> $arquivo

vim $arquivo
