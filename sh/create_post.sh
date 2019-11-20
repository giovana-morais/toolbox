#!/bin/bash

# script pra criar header dos posts do Jekyll já com a data certa

nome_arquivo=$1
data_arquivo=$(date +"%Y-%m-%d")

arquivo="${data_arquivo}-${nome_arquivo}.md"

{
	echo "Criando arquivo $arquivo"
	"---"
	"title: "
	"layout: post"
	"date: $(date +"%y-%m-%d %h:%m")"
	"image: "
	"headerimage: false"
	"tag: "
	"category: blog"
	"author: giovanamorais"
	"description: "
	"---"
} >> "$arquivo"

vim "$arquivo"
