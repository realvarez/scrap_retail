#!/bin/bash
app="retail_scrapping:0.1"
docker build -t ${app} .
docker run --rm --name selenium-scrapping --memory=1g -v "${PWD}/output":"/output/" ${app}
