#!/bin/bash


str=$( pip freeze | grep -i semgrep )

echo $str