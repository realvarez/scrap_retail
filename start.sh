#!/bin/bash
app="test-scrapping:0.1"
docker build -t ${app} .
docker run --rm --name selenium-scrapping --memory=1g -v "C:\Users\Ricardo Alvarez\Proyectos\scrapping\output":"/output/" ${app}
