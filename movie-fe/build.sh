#!/bin/bash

rm -rf ./build
rm -rf ../server/static
rm -rf ../server/templates

mkdir -p ../server/static
mkdir -p ../server/templates

node scripts/build.js

cd ./build

cp -a ./*.html ../../server/templates
cp -a ./* ../../server/static

rm -rf ../../server/static/*.html

echo 'Build complete'

